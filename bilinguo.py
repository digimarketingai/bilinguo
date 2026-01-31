import gradio as gr
import pandas as pd
from gtts import gTTS

SUPPORTED_LANGS = {
    "en": "English",
    "zh-TW": "繁體中文",
    "zh-CN": "简体中文",
    "ja": "日本語",
    "ko": "한국어",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "th": "ไทย",
    "vi": "Tiếng Việt"
}

class Bilinguo:
    def __init__(self):
        self.title = "Bilinguo"
        self.developer = "Anonymous"
        self.lang_a = "en"
        self.lang_b = "zh-TW"
        self.lang_a_name = "English"
        self.lang_b_name = "繁體中文"
        self.df = None
        self.glossary_a = {}
        self.glossary_b = {}
        self.term_list = []

    def set_title(self, title):
        self.title = title

    def set_developer(self, name):
        self.developer = name

    def set_languages(self, lang_a, lang_b):
        if lang_a == lang_b:
            raise ValueError("Must be two different languages! 必須是兩種不同語言！")
        if lang_a not in SUPPORTED_LANGS:
            raise ValueError(f"Language '{lang_a}' not supported. 不支援此語言。")
        if lang_b not in SUPPORTED_LANGS:
            raise ValueError(f"Language '{lang_b}' not supported. 不支援此語言。")
        self.lang_a = lang_a
        self.lang_b = lang_b
        self.lang_a_name = SUPPORTED_LANGS[lang_a]
        self.lang_b_name = SUPPORTED_LANGS[lang_b]

    def _load_csv(self, file):
        self.df = pd.read_csv(file)
        col_a = self.df.iloc[:, 0].astype(str).str.strip()
        col_b = self.df.iloc[:, 1].astype(str).str.strip()
        
        # Build glossaries
        self.glossary_a = dict(zip(col_a.str.lower(), col_b))
        self.glossary_b = dict(zip(col_b, col_a))
        
        # Build clickable term list
        self.term_list = [f"{a}  ↔  {b}" for a, b in zip(col_a, col_b)]
        
        status = f"✓ 已載入 Loaded {len(self.glossary_a)} 術語 terms"
        
        return status, gr.update(choices=self.term_list, value=None)

    def _search(self, term):
        if not term:
            return "請輸入術語 Please enter a term", None
        
        term = term.strip()
        result = self.glossary_a.get(term.lower()) or self.glossary_b.get(term)
        
        if not result:
            return "查無此詞 Not found", None
        
        # Determine TTS language
        if term.lower() in self.glossary_a:
            tts_lang = self.lang_b
        else:
            tts_lang = self.lang_a
        
        # Generate audio
        try:
            tts = gTTS(result, lang=tts_lang)
            tts.save("audio.mp3")
            audio = "audio.mp3"
        except:
            audio = None
        
        return result, audio

    def _click_term(self, selected):
        if not selected:
            return "", "", None
        
        # Parse selected term "termA  ↔  termB"
        parts = selected.split("  ↔  ")
        if len(parts) != 2:
            return "", "", None
        
        term_a, term_b = parts[0].strip(), parts[1].strip()
        
        # Generate audio for term B (target language)
        try:
            tts = gTTS(term_b, lang=self.lang_b)
            tts.save("audio.mp3")
            audio = "audio.mp3"
        except:
            audio = None
        
        return term_a, term_b, audio

    def _filter_list(self, query):
        if not query or not self.term_list:
            return gr.update(choices=self.term_list)
        
        query = query.lower()
        filtered = [t for t in self.term_list if query in t.lower()]
        return gr.update(choices=filtered)

    def launch(self):
        with gr.Blocks(title=self.title, theme=gr.themes.Soft()) as demo:
            
            # Header
            gr.Markdown(f"# 🌐 {self.title}")
            gr.Markdown(f"*開發者 Developer: {self.developer}*")
            gr.Markdown(f"**{self.lang_a_name} ↔ {self.lang_b_name}**")
            
            # File upload
            with gr.Row():
                file = gr.File(label="📁 上傳CSV / Upload CSV", file_types=[".csv"])
                status = gr.Textbox(label="狀態 Status", interactive=False)
            
            gr.Markdown("---")
            
            # Main layout: sidebar + main area
            with gr.Row():
                
                # Left sidebar: term list
                with gr.Column(scale=1):
                    gr.Markdown("### 📋 術語列表 Term List")
                    filter_box = gr.Textbox(
                        label="🔍 篩選 Filter",
                        placeholder="輸入關鍵字 Type to filter..."
                    )
                    term_list_radio = gr.Radio(
                        choices=[],
                        label="點擊選擇 Click to Select",
                        interactive=True
                    )
                
                # Right main area: search + results
                with gr.Column(scale=2):
                    gr.Markdown("### 🔎 搜尋 Search")
                    
                    with gr.Row():
                        search_box = gr.Textbox(
                            label=f"輸入術語 Enter Term ({self.lang_a_name} or {self.lang_b_name})",
                            placeholder="輸入術語... Type a term..."
                        )
                        search_btn = gr.Button("🔍 搜尋 Search", variant="primary")
                    
                    gr.Markdown("### 📖 結果 Result")
                    
                    with gr.Row():
                        result_a = gr.Textbox(label=self.lang_a_name, interactive=False)
                        result_b = gr.Textbox(label=self.lang_b_name, interactive=False)
                    
                    audio = gr.Audio(label="🔊 發音 Pronunciation")
            
            # Event handlers
            
            # File upload → load glossary + populate term list
            file.change(
                fn=self._load_csv,
                inputs=file,
                outputs=[status, term_list_radio]
            )
            
            # Filter box → filter term list
            filter_box.change(
                fn=self._filter_list,
                inputs=filter_box,
                outputs=term_list_radio
            )
            
            # Click term in list → show both terms + audio
            term_list_radio.change(
                fn=self._click_term,
                inputs=term_list_radio,
                outputs=[result_a, result_b, audio]
            )
            
            # Search button → search + audio
            def search_and_display(term):
                result, audio_file = self._search(term)
                if result == "查無此詞 Not found":
                    return term, result, audio_file
                # Determine which is which
                if term.lower() in self.glossary_a:
                    return term, result, audio_file
                else:
                    return result, term, audio_file
            
            search_btn.click(
                fn=search_and_display,
                inputs=search_box,
                outputs=[result_a, result_b, audio]
            )
            
            # Also trigger search on Enter key
            search_box.submit(
                fn=search_and_display,
                inputs=search_box,
                outputs=[result_a, result_b, audio]
            )
        
        demo.launch()

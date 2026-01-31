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
        self.glossary_a = {}
        self.glossary_b = {}

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
        df = pd.read_csv(file)
        col_a = df.iloc[:, 0].astype(str).str.strip()
        col_b = df.iloc[:, 1].astype(str).str.strip()
        self.glossary_a = dict(zip(col_a.str.lower(), col_b))
        self.glossary_b = dict(zip(col_b, col_a))
        return f"✓ 已載入 Loaded {len(self.glossary_a)} 術語 terms"

    def _search(self, term):
        term = term.strip()
        result = self.glossary_a.get(term.lower()) or self.glossary_b.get(term)
        if not result:
            return "查無此詞 Not found", None
        is_lang_b = result in self.glossary_b
        tts_lang = self.lang_b if is_lang_b else self.lang_a
        try:
            gTTS(result, lang=tts_lang).save("audio.mp3")
            audio = "audio.mp3"
        except:
            audio = None
        return result, audio

    def launch(self):
        with gr.Blocks(title=self.title) as demo:
            gr.Markdown(f"# {self.title}")
            gr.Markdown(f"*開發者 Developer: {self.developer}*")
            gr.Markdown(f"🌐 {self.lang_a_name} ↔ {self.lang_b_name}")
            file = gr.File(label="上傳CSV / Upload CSV")
            status = gr.Textbox(label="狀態 Status")
            file.change(self._load_csv, file, status)
            term = gr.Textbox(label="輸入術語 / Enter Term")
            result = gr.Textbox(label="結果 Result")
            audio = gr.Audio()
            gr.Button("搜尋 Search").click(self._search, term, [result, audio])
        demo.launch()

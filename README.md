# 🌐 Bilinguo

Build bilingual termbases with audio. Fast. Simple.
快速建立雙語術語庫，含語音功能。

---

## Installation 安裝

```python
!pip install git+https://github.com/digimarketingai/bilinguo.git -q
```

---

## Usage 使用方法

```python
from bilinguo import Bilinguo

# Initialize 初始化
app = Bilinguo()

# Configure 設定
app.set_title("My Termbase")
app.set_developer("Your Name")
app.set_languages("en", "zh-TW")

# Run 執行
app.launch()
```

---

## Configuration Options 設定選項

### `set_title(title: str)`
Set app title. 設定應用程式標題。
```python
app.set_title("醫學術語庫 Medical Termbase")
```

### `set_developer(name: str)`
Set developer name. 設定開發者名稱。
```python
app.set_developer("Dr. Chen 陳醫師")
```

### `set_languages(lang_a: str, lang_b: str)`
Set language pair. 設定語言配對。
```python
app.set_languages("en", "ja")  # English ↔ 日本語
```

---

## Supported Languages 支援語言

```
en      English
zh-TW   繁體中文
zh-CN   简体中文
ja      日本語
ko      한국어
de      Deutsch
fr      Français
es      Español
th      ไทย
vi      Tiếng Việt
```

---

## CSV Format CSV格式

```csv
English,繁體中文
hello,你好
goodbye,再見
thank you,謝謝
```

> Column headers can be anything. 欄位標題可自訂。
> Column 1 = lang_a, Column 2 = lang_b

---

## Full Example 完整範例

```python
# Install
!pip install git+https://github.com/digimarketingai/bilinguo.git -q

# Import
from bilinguo import Bilinguo

# Create app
app = Bilinguo()

# Settings
app.set_title("中醫術語庫 TCM Termbase")
app.set_developer("王醫師 Dr. Wang")
app.set_languages("en", "zh-TW")

# Launch
app.launch()
```

---

## License

MIT
```

---

## 4. `example.csv`

```csv
English,繁體中文
acupuncture,針灸
moxibustion,艾灸
meridian,經絡
qi,氣
herbal medicine,中藥
pulse diagnosis,脈診
cupping therapy,拔罐
yin,陰
yang,陽
five elements,五行
```

---

## 5. Student Code 學生程式碼

```python
###############################################
#  🌐 Bilinguo - Bilingual Termbase Builder
#  雙語術語庫建立工具
###############################################

# ============ INSTALL 安裝 ============
!pip install git+https://github.com/digimarketingai/bilinguo.git -q

# ============ IMPORT 匯入 ============
from bilinguo import Bilinguo

# ============ SETTINGS 設定區 ============
# 👇 Modify these values 修改以下設定

TITLE     = "中醫術語庫 TCM Termbase"    # App title 應用程式標題
DEVELOPER = "Your Name 你的名字"          # Your name 你的名字
LANG_A    = "en"                          # Language A 語言A
LANG_B    = "zh-TW"                        # Language B 語言B

# ============ BUILD APP 建立應用程式 ============
app = Bilinguo()
app.set_title(TITLE)
app.set_developer(DEVELOPER)
app.set_languages(LANG_A, LANG_B)

# ============ LAUNCH 啟動 ============
app.launch()
```

---

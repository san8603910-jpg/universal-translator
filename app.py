import streamlit as st
from deep_translator import GoogleTranslator
import urllib.parse

# 1. Page Configuration
st.set_page_config(
    page_title="Anuvaad AI", 
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. कड़क CSS स्टाइल (लैपटॉप और मोबाइल दोनों के लुक के लिए)
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 600px; padding-top: 1rem; }
    h1 { color: #0072ff; text-align: center; font-family: 'Segoe UI', sans-serif; margin-bottom: 0px; }
    p.subtitle { text-align: center; color: #555; margin-bottom: 20px; }
    
    /* यूटिलिटी बटन्स (Space, Back, Clear) के लिए स्टाइल */
    div.stButton > button {
        width: 100% !important;
        height: 45px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        background-color: #f8f9fa !important;
        border: 1px solid #ced4da !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# स्टेट मैनेजमेंट
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

# क्वेरी पैरामीटर से कीबोर्ड इनपुट पकड़ना (यह बिना लेआउट बिगाड़े काम करता है)
query_params = st.query_params
if "add_key" in query_params:
    clicked_key = query_params["add_key"]
    # पैरामीटर को तुरंत साफ करना ताकि रीलोड पर बार-बार टाइप न हो
    st.query_params.clear()
    
    if clicked_key == "SPACE":
        st.session_state.typed_text += " "
    elif clicked_key == "BACK":
        st.session_state.typed_text = st.session_state.typed_text[:-1]
    elif clicked_key == "CLEAR":
        st.session_state.typed_text = ""
    else:
        st.session_state.typed_text += clicked_key
    st.rerun()

# टॉप 10 भाषाएँ
languages = {
    'English': 'en',
    'Mandarin Chinese': 'zh-CN',
    'Hindi': 'hi',
    'Spanish': 'es',
    'French': 'fr',
    'Standard Arabic': 'ar',
    'Bengali': 'bn',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Urdu': 'ur'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Typing Language (लिखने की भाषा):", list(languages.keys()))
with col2:
    target_lang = st.selectbox("Target Language (अनुवाद की भाषा):", list(languages.keys()), index=2)

st.write("---")

is_rtl = "Arabic" in source_lang or "Urdu" in source_lang
text_align = "right" if is_rtl else "left"

# मुख्य इनपुट बॉक्स
user_input = st.text_input("Type here or use the keyboard below:", value=st.session_state.typed_text)
if user_input != st.session_state.typed_text:
    st.session_state.typed_text = user_input

st.write("⌨️ **On-Screen Keyboard:**")

# --- भाषाओं के सटीक लेआउट्स ---
if "Hindi" in source_lang:
    rows = [
        ['अ', 'आ', 'इ', 'ई', 'う', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ'],
        ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ'],
        ['ट', 'ठ', 'ड', 'ढ', 'त', 'थ', 'द', 'ध'],
        ['न', 'प', 'ফ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व']
    ]
elif "Bengali" in source_lang:
    rows = [
        ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'এ', 'ঐ', 'ও', 'ঔ'],
        ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ঝ'],
        ['ট', 'ঠ', 'ড', 'ঢ', 'ত', 'থ', 'দ', 'ধ'],
        ['ন', 'প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ']
    ]
elif "Mandarin Chinese" in source_lang:
    rows = [
        ['你', '好', '吗', '我', '喜', '欢'],
        ['中', '国', '人', '谢', '谢', '不'],
        ['客', '气', '再', '见', '是', '的']
    ]
elif "Standard Arabic" in source_lang:
    rows = [
        ['ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه'],
        ['خ', 'ح', 'ج', 'ش', 'س', 'ي', 'ب', 'ل'],
        ['ا', 'ت', 'ن', 'م', 'ك', 'ط', 'ئ', 'ء']
    ]
elif "Urdu" in source_lang:
    rows = [
        ['ق', 'و', 'ر', 'ٹ', 'ے', 'ہ', 'او', 'پ'],
        ['ا', 'س', 'د', 'ف', 'گ', 'ھ', 'ج', 'ک'],
        ['ل', 'ز', 'خ', 'چ', 'ب', 'ন', 'م', 'ت']
    ]
elif "Russian" in source_lang:
    rows = [
        ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш'],
        ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л'],
        ['д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и']
    ]
elif "Spanish" in source_lang:
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'á', 'é', 'í']
    ]
elif "French" in source_lang:
    rows = [
        ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
        ['w', 'x', 'c', 'v', 'b', 'n', 'é', 'è', 'à', 'ç']
    ]
elif "Portuguese" in source_lang:
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'ã', 'õ', 'á']
    ]
else:
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

# 3. HTML/CSS कीबोर्ड बनाना जो कभी नहीं टूटेगा
html_code = """
<style>
    .keyboard {
        display: flex;
        flex-direction: column;
        gap: 6px;
        background-color: #f1f3f4;
        padding: 10px;
        border-radius: 8px;
        font-family: sans-serif;
    }
    .keyboard-row {
        display: flex;
        justify-content: center;
        gap: 4px;
        width: 100%;
    }
    .key-btn {
        flex: 1;
        height: 42px;
        font-size: 16px;
        font-weight: bold;
        background: white;
        border: 1px solid #ced4da;
        border-radius: 5px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        text-decoration: none;
        color: black;
    }
    .key-btn:active {
        background: #0072ff;
        color: white;
    }
</style>
<div class="keyboard">
"""

for row in rows:
    html_code += '<div class="keyboard-row">'
    for key in row:
        encoded_key = urllib.parse.quote(key)
        # बटन पर क्लिक करते ही पैरेंट विंडो का URL पैरामीटर अपडेट होगा जिससे स्ट्रीमलिट को इनपुट मिल जाएगा
        html_code += f'<a class="key-btn" target="_parent" href="?add_key={encoded_key}">{key}</a>'
    html_code += '</div>'

html_code += "</div>"

# ऑन-स्क्रीन कीबोर्ड रेंडर करना
st.components.v1.html(html_code, height=210)

# 4. स्पेशल यूटिलिटी कीज (Space, Back, Clear) - ये स्ट्रीमलिट के ही रहेंगे क्योंकि ये 3 ही बटन हैं, तो मोबाइल पर नहीं टूटेंगे
st.write("")
col_sp, col_bk, col_cl = st.columns([2, 1, 1])
if col_sp.button("Space ␣", key="key_space"):
    st.session_state.typed_text = " " + st.session_state.typed_text if is_rtl else st.session_state.typed_text + " "
    st.rerun()
if col_bk.button("⌫ Back", key="key_back"):
    st.session_state.typed_text = st.session_state.typed_text[1:] if is_rtl else st.session_state.typed_text[:-1]
    st.rerun()
if col_cl.button("🗑️ Clear All", key="key_clear"):
    st.session_state.typed_text = ""
    st.rerun()

st.write("---")

# 5. ट्रांसलेशन लॉजिक
if st.session_state.typed_text:
    st.markdown(f"<div style='text-align: {text_align}; padding: 12px; background-color: #e8f0fe; border-radius: 6px; font-size: 16px;'><b>Your Text:</b> {st.session_state.typed_text}</div>", unsafe_allow_html=True)
    st.write("")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(st.session_state.typed_text)
        st.success(f"**Translation (अनुवाद):** {translated}")
    except Exception as e:
        st.error("अनुवाद करने में कुछ दिक्कत आई।")

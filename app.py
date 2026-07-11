import streamlit as st
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(
    page_title="Anuvaad AI", 
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS (मोबाइल रिस्पॉन्सिव कीबोर्ड के लिए जादुई कोड)
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 600px; padding-top: 2rem; }
    h1 { color: #0072ff; text-align: center; font-family: 'Segoe UI', sans-serif; margin-bottom: 0px; }
    p.subtitle { text-align: center; color: #555; margin-bottom: 20px; }
    
    /* कीबोर्ड कंटेनर डिज़ाइन */
    .keyboard-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        background-color: #f1f3f4;
        padding: 12px;
        border-radius: 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 10px;
    }
    
    /* हर पंक्ति (Row) को सेट करना जो कभी भी टूटेगी नहीं */
    .keyboard-row {
        display: flex;
        justify-content: center;
        width: 100%;
        gap: 5px;
    }
    
    /* बट्टों को कस्टमाइज़ करना */
    div.stButton > button {
        width: 100% !important;
        height: 42px !important;
        min-width: 25px !important;
        padding: 0px !important;
        margin: 0px !important;
        font-size: 15px !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        background-color: #ffffff !important;
        border: 1px solid #ced4da !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    div.stButton > button:hover {
        border-color: #0072ff !important;
        background-color: #f8f9fa !important;
    }
    
    div.stButton > button:active {
        background-color: #0072ff !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# स्टेट मैनेजमेंट
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

# 3. टॉप 10 भाषाएँ
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

# 4. इनपुट बॉक्स
user_input = st.text_input("Type here or use the keyboard below:", value=st.session_state.typed_text)
if user_input != st.session_state.typed_text:
    st.session_state.typed_text = user_input

st.write("⌨️ **On-Screen Keyboard:**")

# 5. लेआउट्स को पंक्तियों में सेट करना (थोड़ा छोटा लेआउट ताकि मोबाइल पर एकदम फिट आए)
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
        ['ট', 'ठ', 'ড', 'ঢ', 'ত', 'থ', 'দ', 'ধ'],
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
        ['ل', 'ز', 'خ', 'چ', 'ب', 'ن', 'م', 'ت']
    ]
elif "Russian" in source_lang:
    rows = [
        ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш'],
        ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л'],
        ['д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и']
    ]
else:
    # English, Spanish, French, Portuguese (Standard QWERTY 3 Rows)
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

# HTML डिज़ाइन कंटेनर की शुरुआत (बैकएंड पर सुंदर दिखाने के लिए)
st.markdown('<div class="keyboard-container">', unsafe_allow_html=True)

for r_idx, row in enumerate(rows):
    # हर पंक्ति के लिए अलग कॉलम ताकि बटन साइड-बाय-साइड रहें
    cols = st.columns(len(row))
    for idx, key in enumerate(row):
        if cols[idx].button(key, key=f"btn_{source_lang}_{r_idx}_{idx}_{key}"):
            if is_rtl:
                st.session_state.typed_text = key + st.session_state.typed_text
            else:
                st.session_state.typed_text += key
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# स्पेशल यूटिलिटी कीज (Space, Backspace, Clear)
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

# 6. ट्रांसलेशन लॉजिक
if st.session_state.typed_text:
    st.markdown(f"<div style='text-align: {text_align}; padding: 12px; background-color: #e8f0fe; border-radius: 6px; font-size: 16px;'><b>Your Text:</b> {st.session_state.typed_text}</div>", unsafe_allow_html=True)
    st.write("")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(st.session_state.typed_text)
        st.success(f"**Translation (अनुवाद):** {translated}")
    except Exception as e:
        st.error("अनुवाद करने में कुछ दिक्कत आई। कृपया दोबारा प्रयास करें।")

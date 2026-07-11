import streamlit as st
from deep_translator import GoogleTranslator

# 1. Page Configuration (बिल्कुल टॉप पर)
st.set_page_config(
    page_title="Anuvaad AI", 
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS (बटनों को कीबोर्ड जैसा लुक देने के लिए)
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 600px; }
    h1 { color: #0072ff; text-align: center; font-family: 'Segoe UI', sans-serif; }
    p.subtitle { text-align: center; color: #555; margin-bottom: 20px; }
    /* बटनों को कीबोर्ड की तरह पास-पास और सुंदर बनाने के लिए */
    div.stButton > button {
        width: 100% !important;
        padding: 6px 2px !important;
        margin: 2px 0px !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# टाइप किए गए टेक्स्ट को याद रखने के लिए (Session State)
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

# 3. सभी भाषाओं की लिस्ट
languages = {
    'English': 'en',
    'Hindi (हिंदी)': 'hi',
    'Spanish (Español)': 'es',
    'French (Français)': 'fr',
    'German (Deutsch)': 'de',
    'Italian (Italiano)': 'it',
    'Portuguese (Português)': 'pt',
    'Russian (Русский)': 'ru',
    'Chinese (中文)': 'zh-CN',
    'Japanese (日本語)': 'ja',
    'Korean (한국어)': 'ko',
    'Arabic (العربية)': 'ar',
    'Bengali (বাংলা)': 'bn',
    'Marathi (मराठी)': 'mr',
    'Telugu (తెలుగు)': 'te',
    'Tamil (தமிழ்)': 'ta',
    'Gujarati (ગુજરાતી)': 'gu',
    'Urdu (اُردو)': 'ur'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Typing Language (लिखने की भाषा):", list(languages.keys()))
with col2:
    target_lang = st.selectbox("Target Language (अनुवाद की भाषा):", list(languages.keys()), index=1)

st.write("---")

# 4. इनपुट बॉक्स (जो कीबोर्ड से सीधे कनेक्टेड है)
user_input = st.text_input("Type here or use the on-screen keyboard below (यहाँ टाइप करें):", value=st.session_state.typed_text)

# अगर यूजर खुद कीबोर्ड से टाइप करे तो वैल्यू सिंक करें
if user_input != st.session_state.typed_text:
    st.session_state.typed_text = user_input

# 5. ऑन-स्क्रीन कीबोर्ड लेआउट जेनरेट करना
st.write("⌨️ **On-Screen Keyboard:**")

if "Hindi" in source_lang:
    # हिंदी वर्णमाला लेआउट
    row1 = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ']
    row2 = ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ट', 'ठ']
    row3 = ['ड', 'ढ', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब']
    row4 = ['भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह']
    
    for row in [row1, row2, row3, row4]:
        cols = st.columns(len(row))
        for idx, key in enumerate(row):
            if cols[idx].button(key, key=f"hi_{key}_{idx}"):
                st.session_state.typed_text += key
                st.rerun()
else:
    # इंग्लिश/चाइनीज पिनयिन/अन्य सभी भाषाओं के लिए यूनिवर्सल QWERTY लेआउट
    row1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    row2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    row3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    
    for row in [row1, row2, row3]:
        cols = st.columns(len(row))
        for idx, key in enumerate(row):
            if cols[idx].button(key, key=f"en_{key}_{idx}"):
                st.session_state.typed_text += key
                st.rerun()

# स्पेशल कीज (Space, Backspace, Clear)
st.write("")
col_sp, col_bk, col_cl = st.columns([2, 1, 1])
if col_sp.button("Space ␣", key="key_space"):
    st.session_state.typed_text += " "
    st.rerun()
if col_bk.button("⌫ Back", key="key_back"):
    st.session_state.typed_text = st.session_state.typed_text[:-1]
    st.rerun()
if col_cl.button("🗑️ Clear All", key="key_clear"):
    st.session_state.typed_text = ""
    st.rerun()

st.write("---")

# 6. ट्रांसलेशन लॉजिक (बिना किसी एरर के)
if st.session_state.typed_text:
    st.info(f"**Your Text (आपका टेक्स्ट):** {st.session_state.typed_text}")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(st.session_state.typed_text)
        st.success(f"**Translation (अनुवाद):** {translated}")
    except Exception as e:
        st.error("अनुवाद करने में कुछ दिक्कत आई। कृपया दोबारा प्रयास करें।")

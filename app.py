import streamlit as st
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(
    page_title="Anuvaad AI", 
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS (कीबोर्ड बटनों को सुंदर बनाने के लिए)
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 600px; }
    h1 { color: #0072ff; text-align: center; font-family: 'Segoe UI', sans-serif; }
    p.subtitle { text-align: center; color: #555; margin-bottom: 20px; }
    
    /* बटन स्टाइलिंग */
    div.stButton > button {
        width: 100% !important;
        height: 42px !important;
        padding: 0px !important;
        margin: 2px 0px !important;
        font-size: 15px !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        background-color: #f8f9fa !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: 0.1s;
    }
    div.stButton > button:active {
        background-color: #e2e6ea !important;
        transform: scale(0.95);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# स्टेट मैनेजमेंट (ताकि टाइप किया हुआ डेटा डिलीट न हो)
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

# 3. सभी भाषाओं की लिस्ट
languages = {
    'English': 'en',
    'Hindi (हिंदी)': 'hi',
    'Chinese (中文)': 'zh-CN',
    'Spanish (Español)': 'es',
    'French (Français)': 'fr',
    'German (Deutsch)': 'de',
    'Russian (Русский)': 'ru',
    'Arabic (العربية)': 'ar',
    'Japanese (日本語)': 'ja',
    'Italian (Italiano)': 'it',
    'Marathi (मराठी)': 'mr',
    'Bengali (বাংলা)': 'bn'
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Typing Language (लिखने की भाषा):", list(languages.keys()))
with col2:
    target_lang = st.selectbox("Target Language (अनुवाद की भाषा):", list(languages.keys()), index=1)

st.write("---")

# 4. इनपुट बॉक्स
user_input = st.text_input("Type here or use the keyboard below:", value=st.session_state.typed_text)
if user_input != st.session_state.typed_text:
    st.session_state.typed_text = user_input

st.write("⌨️ **On-Screen Keyboard:**")

# 5. डायनेमिक कीबोर्ड लेआउट्स (Dynamic Keyboard Layouts)
if "Hindi" in source_lang or "Marathi" in source_lang:
    rows = [
        ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ', 'अं'],
        ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ट', 'ठ'],
        ['ड', 'ढ', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब'],
        ['भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह']
    ]
elif "Chinese" in source_lang:
    # चीनी भाषा के लिए सबसे ज़्यादा इस्तेमाल होने वाले फ्रेज/कैरेक्टर्स डायरेक्ट बटन पर
    rows = [
        ['你', '好', '吗', '我', '很', '喜', '欢', '中', '国'],
        ['谢', '谢', '不', '客', '气', '再', '见', '是', '的'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    ]
elif "Russian" in source_lang:
    rows = [
        ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х'],
        ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
        ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю']
    ]
elif "Arabic" in source_lang:
    rows = [
        ['ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه', 'خ', 'ح', 'ج'],
        ['ش', 'س', 'ي', 'ب', 'ل', 'ا', 'ت', 'ن', 'م', 'ك', 'ط'],
        ['ئ', 'ء', 'ؤ', 'ر', 'لا', 'ى', 'ة', 'و', 'ز', 'ظ']
    ]
elif "Japanese" in source_lang:
    rows = [
        ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ'],
        ['さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と'],
        ['な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ'],
        ['ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り']
    ]
else:
    # बाकी सब के लिए यूनिवर्सल QWERTY (English, French, Spanish, German)
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

# कीबोर्ड बटन स्क्रीन पर रेंडर करना
for row in rows:
    cols = st.columns(len(row))
    for idx, key in enumerate(row):
        if cols[idx].button(key, key=f"k_{source_lang}_{key}_{idx}"):
            st.session_state.typed_text += key
            st.rerun()

# स्पेशल यूटिलिटी कीज (Space, Backspace, Clear)
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

# 6. ट्रांसलेशन लॉजिक
if st.session_state.typed_text:
    st.info(f"**Your Text (आपका टेक्स्ट):** {st.session_state.typed_text}")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(st.session_state.typed_text)
        st.success(f"**Translation (अनुवाद):** {translated}")
    except Exception as e:
        st.error("अनुवाद करने में कुछ दिक्कत आई। कृपया दोबारा प्रयास करें।")

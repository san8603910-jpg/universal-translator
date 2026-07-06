import streamlit as st
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(
    page_title="Universal Smart Translator",
    page_icon="🔮",
    layout="centered"
)

# 2. Premium Custom CSS
st.markdown("""
    <style>
    .main-title {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        color: #555555;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .output-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #0072ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        font-size: 1.2rem;
        color: #2c3e50;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔮 Anuvaad AI Ultimate</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">All Languages support</div>', unsafe_allow_html=True)

# 3. दुनिया की सभी भाषाओं को ऑटोमैटिकली लोड करना
try:
    lang_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    display_languages = {k.title(): v for k, v in lang_dict.items()}
except Exception:
    # बैकअप अगर इंटरनेट धीमा हो
    display_languages = {"English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr"}

sorted_lang_names = sorted(list(display_languages.keys()))
default_index = sorted_lang_names.index("English") if "English" in sorted_lang_names else 0

# Language Dropdown (अब इसमें सभी भाषाएँ दिखेंगी)
target_lang_name = st.selectbox(
    "🎯 Select Target Language :",
    options=sorted_lang_names,
    index=default_index
)
target_lang_code = display_languages[target_lang_name]

# Text input
source_text = st.text_area(
    "📥 Enter Text :", 
    placeholder="जैसे लिखें: 'namaste', 'aap kaise ho', 'where are you'...",
    height=150
)

# 💡 कॉमन हिंग्लिश शब्दों के लिए लोकल डिक्शनरी मैपिंग
HINGLISH_MAP = {
    "namaste": "Hello / Greetings",
    "namaskar": "Hello / Greetings",
    "kaise ho": "How are you?",
    "aap kaise ho": "How are you?",
    "kya kar rahe ho": "What are you doing?",
    "kya chal raha hai": "What's going on?",
    "shukriya": "Thank you",
    "dhanyawad": "Thank you",
    "alvida": "Goodbye",
    "haan": "Yes",
    "na": "No",
    "nahi": "No"
}

# Translate Button
if st.button("Translate ✨", type="primary"):
    cleaned_input = source_text.strip().lower().replace("?", "").replace("!", "")
    
    if not source_text.strip():
        st.error("⚠️ Please enter some text first!")
    else:
        with st.spinner(f"Translating to {target_lang_name}..."):
            try:
                # अगर इनपुट डायरेक्ट शॉर्टकट हिंग्लिश है और टारगेट इंग्लिश है
                if cleaned_input in HINGLISH_MAP and target_lang_code == 'en':
                    translated = HINGLISH_MAP[cleaned_input]
                else:
                    # अगर टारगेट इंग्लिश है, तो पहले हिंग्लिश वाक्यों को हिंदी स्क्रिप्ट में बदलेंगे
                    if target_lang_code == 'en':
                        try:
                            hindi_script = GoogleTranslator(source='en', target='hi').translate(source_text)
                            translated = GoogleTranslator(source='hi', target='en').translate(hindi_script)
                            
                            if translated.strip().lower() == source_text.strip().lower():
                                translated = GoogleTranslator(source='auto', target='en').translate(source_text)
                        except:
                            translated = GoogleTranslator(source='auto', target=target_lang_code).translate(source_text)
                    else:
                        # बाकी सभी भाषाओं के लिए नॉर्मल ट्रांसलेशन
                        translated = GoogleTranslator(source='auto', target=target_lang_code).translate(source_text)

                st.markdown(f"### 📤 Output in {target_lang_name}:")
                st.markdown(f'<div class="output-box">{translated}</div>', unsafe_allow_html=True)
                st.toast("Translation complete!", icon="✅")
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
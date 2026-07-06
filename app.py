import streamlit as st
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(
    page_title="Universal Smart Translator",
    page_icon="🔮",
    layout="centered"
)

# 2. Premium Custom CSS (Mobile Optimization + Hide Streamlit Branding)
st.markdown("""
    <style>
    /* 1. स्ट्रीमलिट की ब्रांडिंग और मेनू छुपाने का जादुई कोड */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    div.stActionButton {display: none !important;}
    
    /* 2. बैकग्राउंड और फॉन्ट स्टाइल */
    .main {
        background-color: #f9fbfd;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    /* 3. मोबाइल के लिए टाइटल्स को रेस्पॉन्सिव बनाना */
    .main-title {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: calc(1.8rem + 1.5vw); /* मोबाइल पर छोटा, कंप्यूटर पर बड़ा होगा */
        font-weight: 800;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #666666;
        text-align: center;
        font-size: calc(0.9rem + 0.3vw);
        margin-bottom: 25px;
    }
    
    /* 4. मोबाइल फ्रेंडली आउटपुट बॉक्स */
    .output-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #0072ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        font-size: 1.1rem;
        color: #2c3e50;
        line-height: 1.5;
        margin-top: 10px;
    }
    
    /* 5. इनपुट बॉक्स के टेक्स्ट एरिया को मोबाइल पर बेहतर दिखाना */
    textarea {
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔮 Anuvaad AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instant Universal language Translation</div>', unsafe_allow_html=True)

# 3. Load Supported Languages
try:
    lang_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    display_languages = {k.title(): v for k, v in lang_dict.items()}
except Exception:
    display_languages = {"English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr"}

sorted_lang_names = sorted(list(display_languages.keys()))
default_index = sorted_lang_names.index("English") if "English" in sorted_lang_names else 0

# Language Dropdown
target_lang_name = st.selectbox(
    "🎯 Select Target Language:",
    options=sorted_lang_names,
    index=default_index
)
target_lang_code = display_languages[target_lang_name]

# Text input
source_text = st.text_area(
    "📥 Enter Text:", 
    placeholder="Type or paste text here... (e.g., namaste, kaise ho)",
    height=120
)

# Hinglish Dictionary Mapping
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
if st.button("Translate ✨", type="primary", use_container_width=True): # use_container_width से बटन मोबाइल स्क्रीन पर पूरा फैल जाएगा जो सुंदर दिखता है
    cleaned_input = source_text.strip().lower().replace("?", "").replace("!", "")
    
    if not source_text.strip():
        st.error("⚠️ Please enter some text first!")
    else:
        with st.spinner(f"Translating..."):
            try:
                if cleaned_input in HINGLISH_MAP and target_lang_code == 'en':
                    translated = HINGLISH_MAP[cleaned_input]
                else:
                    if target_lang_code == 'en':
                        try:
                            hindi_script = GoogleTranslator(source='en', target='hi').translate(source_text)
                            translated = GoogleTranslator(source='hi', target='en').translate(hindi_script)
                            if translated.strip().lower() == source_text.strip().lower():
                                translated = GoogleTranslator(source='auto', target='en').translate(source_text)
                        except:
                            translated = GoogleTranslator(source='auto', target=target_lang_code).translate(source_text)
                    else:
                        translated = GoogleTranslator(source='auto', target=target_lang_code).translate(source_text)

                st.markdown(f"### 📤 Output:")
                st.markdown(f'<div class="output-box">{translated}</div>', unsafe_allow_html=True)
                st.toast("Done!", icon="✅")
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")

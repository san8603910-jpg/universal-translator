import streamlit as st
import streamlit.components.v1 as components
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(
    page_title="Anuvaad AI", 
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 600px; }
    h1 { color: #0072ff; text-align: center; font-family: 'Segoe UI', sans-serif; }
    p.subtitle { text-align: center; color: #555; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# 3. दुनिया की सभी मुख्य भाषाओं की लिस्ट (Full Support)
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

# अगर हिंदी चुनी है तो हिंदी लेआउट, बाकी सभी भाषाओं के लिए यूनिवर्सल इंग्लिश लेआउट काम करेगा
layout_type = "hindi" if "Hindi" in source_lang else "english"

# 4. यूनिवर्सल वर्चुअल कीबोर्ड कंपोनेंट
custom_keyboard_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-keyboard@latest/build/css/index.css">
    <style>
        body {{ font-family: sans-serif; margin: 0; padding: 0; background: transparent; }}
        #input_box {{ 
            width: 100%; padding: 14px; font-size: 16px; 
            border: 2px solid #0072ff; border-radius: 8px; 
            box-sizing: border-box; margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .simple-keyboard {{ max-width: 100%; background-color: #f1f3f4; border-radius: 8px; padding: 8px; }}
        .hg-theme-default .hg-button {{ height: 40px; font-size: 14px; }}
    </style>
</head>
<body>

<input id="input_box" placeholder="यहाँ टाइप करें या नीचे कीबोर्ड का उपयोग करें..." />
<div class="simple-keyboard"></div>

<script src="https://cdn.jsdelivr.net/npm/simple-keyboard@latest/build/index.js"></script>
<script>
    const Keyboard = window.SimpleKeyboard.default;
    
    const layouts = {{
        english: {{
            'default': [
                'q w e r t y u i o p',
                'a s d f g h j k l',
                'z x c v b n m {{bksp}}',
                '{{space}}'
            ]
        }},
        hindi: {{
            'default': [
                'अ आ इ ई उ ऊ ए ऐ ओ औ अं अः',
                'क kh ग gh ङ च ch ज jh ञ',
                'ट ठ ड ढ ण त th द dh न',
                'प ph ब bh म य र ल व श',
                'ष स ह क्ष त्र ज्ञ {{bksp}}',
                '{{space}}'
            ]
        }}
    }};

    const myKeyboard = new Keyboard({{
        onChange: input => onChange(input),
        layout: layouts['{layout_type}']
    }});

    function onChange(input) {{
        document.querySelector("#input_box").value = input;
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: input
        }}, '*');
    }}

    document.querySelector("#input_box").addEventListener("input", event => {{
        myKeyboard.setInput(event.target.value);
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: event.target.value
        }}, '*');
    }});
</script>

</body>
</html>
"""

st.write("---")
st.write("⌨️ **On-Screen Keyboard Input:**")

# वर्चुअल कीबोर्ड को रेंडर करना
user_text = components.html(custom_keyboard_html, height=320, scrolling=False)

# 5. ट्रांसलेशन लॉजिक
if user_text:
    st.info(f"**Your Text (आपका टेक्स्ट):** {user_text}")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(user_text)
        st.success(f"**Translation (अनुवाद):** {translated}")
    except Exception as e:
        st.error("अनुवाद करने में कुछ दिक्कत आई। कृपया दोबारा प्रयास करें।")

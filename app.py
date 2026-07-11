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

# 2. Custom CSS (Clean UI के लिए)
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 600px; }
    h1 { color: #0072ff; text-align: center; }
    </style>
""", unsafe_style_blocks=True)

st.title("🔮 Anuvaad AI")
st.write("Instant Universal & Hinglish Translation App")

# 3. भाषा चुनने का ऑप्शन
languages = {
    'English': 'en',
    'Hindi (हिंदी)': 'hi',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de'
}

source_lang = st.selectbox("Select Typing Language (typing की भाषा चुनें):", list(languages.keys()))
target_lang = st.selectbox("Select Target Language (अनुवाद की भाषा चुनें):", list(languages.keys()), index=1)

# कीबोर्ड लेआउट तय करना (हिंदी या इंग्लिश के हिसाब से)
layout_type = "hindi" if "Hindi" in source_lang else "english"

# 4. जादुई वर्चुअल कीबोर्ड (HTML/JS Component)
# यह कंपोनेंट सीधे स्क्रीन पर कीबोर्ड दिखाएगा और टाइप किया हुआ टेक्स्ट स्ट्रीमलिट को वापस भेजेगा
custom_keyboard_html = f"""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-keyboard@latest/build/css/index.css">
<style>
    body {{ font-family: sans-serif; margin: 0; padding: 0; background: transparent; }}
    #input_box {{ width: 100%; padding: 12px; font-size: 16px; border: 2px solid #0072ff; border-radius: 8px; box-sizing: border-box; margin-bottom: 10px; }}
    .simple-keyboard {{ max-width: 100%; background-color: #f1f3f4; border-radius: 8px; padding: 5px; }}
</style>

<input id="input_box" placeholder="Type here using screen keyboard..." />
<div class="simple-keyboard"></div>

<script src="https://cdn.jsdelivr.net/npm/simple-keyboard@latest/build/index.js"></script>
<script>
    const Keyboard = window.SimpleKeyboard.default;
    
    // हिंदी और इंग्लिश के लेआउट्स
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
                'क ख ग घ ङ च छ ज झ ञ',
                'ट ठ ड ढ ण त थ द ध न',
                'प फ ब भ म य र ल व श',
                'ष स ह क्ष त्र ज्ञ  {{bksp}}',
                '{{space}}'
            ]
        }}
    }};

    const myKeyboard = new Keyboard({{
        onChange: input => onChange(input),
        onKeyPress: button => onKeyPress(button),
        layout: layouts['{layout_type}']
    }});

    function onChange(input) {{
        document.querySelector("#input_box").value = input;
        // स्ट्रीमलिट को डेटा भेजना
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: input
        }}, '*');
    }}

    function onKeyPress(button) {{
        if (button === "{{{{shift}}}}" || button === "{{{{lock}}}}") handleShift();
    }}
    
    // इनपुट बॉक्स में मैन्युअल टाइपिंग सिंक करना
    document.querySelector("#input_box").addEventListener("input", event => {{
        myKeyboard.setInput(event.target.value);
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: event.target.value
        }}, '*');
    }});
</script>
"""

# HTML कंपोनेंट को स्ट्रीमलिट में रेंडर करना
st.write("---")
st.write("⌨️ **On-Screen Keyboard Input:**")
user_text = components.html(custom_keyboard_html, height=280, scrolling=False)

# 5. ट्रांसलेशन लॉजिक
if user_text:
    st.info(f"**Your Text:** {user_text}")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(user_text)
        st.success(f"**Translation:** {translated}")
    except Exception as e:
        st.error("Translation error or empty input.")

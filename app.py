import streamlit as st
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(
    page_title="Anuvaad AI", 
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS (मोबाइल और लैपटॉप दोनों पर असली कीबोर्ड लुक)
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 600px; }
    h1 { color: #0072ff; text-align: center; font-family: 'Segoe UI', sans-serif; }
    p.subtitle { text-align: center; color: #555; margin-bottom: 20px; }
    
    /* असली कीबोर्ड कंटेनर - यह कभी टूटने नहीं देगा */
    .custom-kbd-container {
        background-color: #f1f3f4;
        padding: 10px;
        border-radius: 10px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-top: 15px;
    }
    .kbd-row {
        display: flex;
        justify-content: center;
        gap: 4px;
        width: 100%;
    }
    .kbd-btn {
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
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
    .kbd-btn:active {
        background: #0072ff;
        color: white;
    }
    .kbd-btn.special {
        background: #e2e6ea;
        flex: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# स्टेट मैनेजमेंट
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

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

# छुपा हुआ इनपुट सिंक करने के लिए ट्रिक
js_click = st.text_input("Hidden Linker", key="js_click", label_visibility="collapsed")
if js_click:
    if js_click == "SPACE":
        st.session_state.typed_text = " " + st.session_state.typed_text if is_rtl else st.session_state.typed_text + " "
    elif js_click == "BACK":
        st.session_state.typed_text = st.session_state.typed_text[1:] if is_rtl else st.session_state.typed_text[:-1]
    elif js_click == "CLEAR":
        st.session_state.typed_text = ""
    else:
        st.session_state.typed_text = js_click + st.session_state.typed_text if is_rtl else st.session_state.typed_text + js_click
    
    # तुरंत इनपुट रीसेट करना ताकि दोबारा सेम कैरेक्टर दबाया जा सके
    st.components.v1.html("""
        <script>
        var inputs = window.parent.document.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].getAttribute('aria-label') === 'Hidden Linker') {
                inputs[i].value = '';
                inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
        </script>
    """, height=0)
    st.rerun()

# मुख्य दिखने वाला इनपुट बॉक्स
user_input = st.text_input("Type here or use the keyboard below:", value=st.session_state.typed_text)
if user_input != st.session_state.typed_text:
    st.session_state.typed_text = user_input

st.write("⌨️ **On-Screen Keyboard:**")

# भाषा के हिसाब से लेआउट चुनना
if "Hindi" in source_lang:
    rows = [
        ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ'],
        ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ञ'],
        ['ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'দ', 'ध'],
        ['ন', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व']
    ]
elif "Bengali" in source_lang:
    rows = [
        ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'এ', 'ঐ', 'ও', 'ঔ'],
        ['ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ'],
        ['ট', 'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন'],
        ['প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'হ']
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
        ['ا', 'س', 'د', '导', 'گ', 'ھ', 'ج', 'ک'],
        ['ل', 'ز', 'خ', 'چ', 'ب', 'ن', 'م', 'ت']
    ]
elif "Russian" in source_lang:
    rows = [
        ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш'],
        ['щ', 'з', 'х', 'ф', 'ы', 'в', 'а', 'п'],
        ['р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч']
    ]
else:
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

# जावास्क्रिप्ट आधारित फुल रिस्पॉन्सिव कीबोर्ड इंजेक्शन
kbd_html = f"""
<div class="custom-kbd-container">
"""
for row in rows:
    kbd_html += '<div class="kbd-row">'
    for key in row:
        kbd_html += f'<div class="kbd-btn" onclick="sendKey(\'{key}\')">{key}</div>'
    kbd_html += '</div>'

# स्पेशल बटन्स की रो
kbd_html += f"""
    <div class="kbd-row">
        <div class="kbd-btn special" onclick="sendKey('SPACE')">Space ␣</div>
        <div class="kbd-btn special" onclick="sendKey('BACK')">⌫ Back</div>
        <div class="kbd-btn special" onclick="sendKey('CLEAR')">🗑️ Clear</div>
    </div>
</div>

<script>
function sendKey(val) {{
    var inputs = window.parent.document.querySelectorAll('input');
    for (var i = 0; i < inputs.length; i++) {{
        if (inputs[i].getAttribute('aria-label') === 'Hidden Linker') {{
            inputs[i].value = val;
            inputs[i].dispatchEvent(new Event('input', {{ bubbles: true }}));
            break;
        {{
    {{
}}
</script>
"""

# HTML कीबोर्ड को कंपोनेंट के जरिए दिखाना
st.components.v1.html(kbd_html, height=240)

st.write("---")

# 6. ट्रांसलेशन लॉजिक
if st.session_state.typed_text:
    st.markdown(f"<div style='text-align: {text_align}; padding: 12px; background-color: #e8f0fe; border-radius: 6px; font-size: 16px;'><b>Your Text:</b> {st.session_state.typed_text}</div>", unsafe_allow_html=True)
    st.write("")
    try:
        translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(st.session_state.typed_text)
        st.success(f"**Translation (अनुवाद):** {translated}")
    except Exception as e:
        st.error("अनुवाद करने में कुछ दिक्कत आई।")

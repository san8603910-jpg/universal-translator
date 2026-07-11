import streamlit as st
from deep_translator import GoogleTranslator

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Anuvaad AI",
    page_icon="🔮",
    layout="centered"
)

# ============================================================
# 2. GLOBAL STYLES (fonts for every script + polished look)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Bengali:wght@400;600&family=Noto+Sans+Arabic:wght@400;600&family=Noto+Nastaliq+Urdu&family=Noto+Sans+SC:wght@400;600&family=Noto+Sans+JP:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans', 'Noto Sans Devanagari', 'Noto Sans Bengali',
                     'Noto Sans Arabic', 'Noto Nastaliq Urdu', 'Noto Sans SC', sans-serif;
    }

    .app-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 18px;
    }

    .key-btn button {
        font-size: 18px !important;
        padding: 6px 0px !important;
        border-radius: 8px !important;
    }

    .text-preview {
        padding: 14px 16px;
        background-color: #eef2ff;
        border: 1px solid #dbe3ff;
        border-radius: 10px;
        font-size: 17px;
        line-height: 1.6;
        word-wrap: break-word;
    }

    .translation-box {
        padding: 14px 16px;
        background-color: #ecfdf5;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        font-size: 17px;
        line-height: 1.6;
        word-wrap: break-word;
    }

    /* ------------------------------------------------------
       MOBILE FIX: by default Streamlit stacks st.columns()
       vertically (one per line) below ~640px width. This
       breaks the on-screen keyboard layout on phones. We
       force the keyboard rows to stay horizontal and wrap
       like a real keyboard instead.
       ------------------------------------------------------ */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        flex-direction: row !important;
        row-gap: 4px !important;
        column-gap: 4px !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: auto !important;
        min-width: 36px !important;
        flex: 0 1 auto !important;
    }
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: wrap !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: auto !important;
            min-width: 30px !important;
            flex: 0 1 auto !important;
        }
        .key-btn button {
            font-size: 15px !important;
            padding: 4px 2px !important;
            min-width: 30px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🔮 Anuvaad AI")
st.markdown("<p class='app-subtitle'>Instant Universal & Hinglish Translation App</p>", unsafe_allow_html=True)

# ============================================================
# 3. STATE MANAGEMENT
# ============================================================
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""


def add_char(char: str):
    st.session_state.typed_text += char


def add_space():
    st.session_state.typed_text += " "


def backspace():
    st.session_state.typed_text = st.session_state.typed_text[:-1]


def clear_all():
    st.session_state.typed_text = ""


# ============================================================
# 4. TOP 10 LANGUAGES
# ============================================================
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

is_rtl = source_lang in ("Standard Arabic", "Urdu")

# Apply direction dynamically to the main text input so RTL scripts
# (Arabic/Urdu) render and align correctly while typing.
direction_css = "rtl" if is_rtl else "ltr"
text_align_css = "right" if is_rtl else "left"
st.markdown(f"""
<style>
    div[data-testid="stTextInput"] input {{
        direction: {direction_css};
        text-align: {text_align_css};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 5. MAIN INPUT BOX
# Bound directly to session_state via key="typed_text" so typing
# and on-screen keyboard clicks always stay perfectly in sync
# (no manual copy/compare, no cursor-jump glitches).
# ============================================================
st.text_input("Type here or use the keyboard below:", key="typed_text")

st.write("⌨️ **On-Screen Keyboard:**")

# ============================================================
# 6. KEYBOARD LAYOUTS (verified, script-accurate, no cross-mixing)
# ============================================================
if source_lang == "Hindi":
    rows = [
        ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ'],
        ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'ञ'],
        ['ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध'],
        ['न', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व']
    ]
elif source_lang == "Bengali":
    rows = [
        ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'এ', 'ঐ', 'ও', 'ঔ'],
        ['ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ'],
        ['ট', 'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন'],
        ['প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'হ']
    ]
elif source_lang == "Mandarin Chinese":
    rows = [
        ['你', '好', '吗', '我', '喜', '欢'],
        ['中', '国', '人', '谢', '谢', '不'],
        ['客', '气', '再', '见', '是', '的']
    ]
elif source_lang == "Standard Arabic":
    rows = [
        ['ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه'],
        ['خ', 'ح', 'ج', 'ش', 'س', 'ي', 'ب', 'ل'],
        ['ا', 'ت', 'ن', 'م', 'ك', 'ط', 'ئ', 'ء']
    ]
elif source_lang == "Urdu":
    # Fixed: previously contained a Devanagari ('च') and a Bengali ('ন')
    # character by mistake. Now a clean, Urdu-only layout.
    rows = [
        ['ق', 'و', 'ر', 'ٹ', 'ے', 'ہ', 'آ', 'پ'],
        ['ا', 'س', 'د', 'ف', 'گ', 'ھ', 'ج', 'ک'],
        ['ل', 'ز', 'خ', 'ط', 'ب', 'ن', 'م', 'ت']
    ]
elif source_lang == "Russian":
    rows = [
        ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш'],
        ['щ', 'з', 'х', 'ф', 'ы', 'в', 'а', 'п'],
        ['р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч']
    ]
elif source_lang == "Spanish":
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'á', 'é', 'í']
    ]
elif source_lang == "French":
    rows = [
        ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
        ['w', 'x', 'c', 'v', 'b', 'n', 'é', 'è', 'à', 'ç']
    ]
elif source_lang == "Portuguese":
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'ã', 'õ', 'á']
    ]
else:  # English and any other default
    rows = [
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

# ============================================================
# 7. KEYBOARD GRID
# Always appends the logical character; the CSS `direction` set
# above handles correct RTL/LTR visual ordering automatically via
# the browser's Unicode bidi algorithm.
# ============================================================
for r_idx, row in enumerate(rows):
    cols = st.columns(len(row))
    for idx, key in enumerate(row):
        with cols[idx]:
            st.markdown('<div class="key-btn">', unsafe_allow_html=True)
            st.button(key, key=f"k_{source_lang}_{r_idx}_{idx}", on_click=add_char, args=(key,))
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 8. SPECIAL UTILITY KEYS
# ============================================================
st.write("")
col_sp, col_bk, col_cl = st.columns([2, 1, 1])
col_sp.button("Space ␣", key="key_space", on_click=add_space)
col_bk.button("⌫ Back", key="key_back", on_click=backspace)
col_cl.button("🗑️ Clear All", key="key_clear", on_click=clear_all)

st.write("---")

# ============================================================
# 9. TRANSLATION LOGIC
# ============================================================
if st.session_state.typed_text:
    st.markdown(
        f"<div class='text-preview'><b>Your Text:</b> {st.session_state.typed_text}</div>",
        unsafe_allow_html=True
    )
    st.write("")
    try:
        translated = GoogleTranslator(
            source=languages[source_lang],
            target=languages[target_lang]
        ).translate(st.session_state.typed_text)
        st.markdown(
            f"<div class='translation-box'><b>Translation (अनुवाद):</b> {translated}</div>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"अनुवाद करने में दिक्कत आई। कृपया internet connection जांचें। (Details: {e})")

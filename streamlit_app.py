import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="סוכן המסחר שלי",
    page_icon="🤖",
    layout="centered"
)

# -------------------------
# נתוני התחלה
# -------------------------
if "cash" not in st.session_state:
    st.session_state.cash = 10000.0

if "profit" not in st.session_state:
    st.session_state.profit = 0.0

if "holding" not in st.session_state:
    st.session_state.holding = "MSFT"

if "runs" not in st.session_state:
    st.session_state.runs = 0

# כרגע ציוני הדגמה מהגרסה שבנינו
ranking = [
    ("MSFT", 88.1),
    ("NVDA", 84.6),
    ("QQQ", 77.3),
    ("SPY", 77.2),
    ("AAPL", 72.6),
]

# -------------------------
# עיצוב
# -------------------------
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }

    h1, h2, h3, p {
        text-align: right;
    }

    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 22px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# כותרת
# -------------------------
st.title("🤖 סוכן המסחר שלי")
st.caption("מערכת ניסוי למסחר וירטואלי בלבד")

st.divider()

# -------------------------
# מצב התיק
# -------------------------
st.subheader("💰 מצב התיק")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "שווי תיק",
        f"₪{st.session_state.cash:,.2f}"
    )

with col2:
    st.metric(
        "רווח / הפסד",
        f"₪{st.session_state.profit:,.2f}"
    )

st.write(f"📌 **מחזיק כרגע:** {st.session_state.holding}")

st.divider()

# -------------------------
# הפעלת הסוכן
# -------------------------
if st.button("▶️ הפעל את סוכן המסחר"):
    st.session_state.runs += 1

    best_symbol = ranking[0][0]
    best_score = ranking[0][1]

    st.session_state.holding = best_symbol

    st.success("✅ הסוכן סיים לבדוק את השוק")

    st.write("### 🤖 החלטת הסוכן")
    st.write(f"🔵 **החזק {best_symbol}**")
    st.write(
        f"הנכס בעל הציון הגבוה ביותר כרגע הוא "
        f"**{best_symbol} — {best_score}**"
    )

    st.write(
        "🕒 בדיקה אחרונה:",
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

st.divider()

# -------------------------
# דירוג
# -------------------------
st.subheader("🏆 דירוג הנכסים")

for number, (symbol, score) in enumerate(ranking, start=1):
    st.write(f"**{number}. {symbol}** — ציון {score}")

st.divider()

st.info(
    "⚠️ כרגע המערכת היא סביבת ניסוי בלבד. "
    "היא אינה קונה או מוכרת ניירות ערך בכסף אמיתי."
)

st.caption(
    f"מספר בדיקות שבוצעו באפליקציה: {st.session_state.runs}"
)

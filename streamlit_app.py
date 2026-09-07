import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="סוכן המסחר שלי",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
.stApp { direction: rtl; }
h1, h2, h3, p { text-align: right; }
</style>
""", unsafe_allow_html=True)

STARTING_CASH = 10000.0
STOCKS = [
    "MSFT", "NVDA", "AAPL", "AMZN",
    "GOOGL", "META", "TSLA", "QQQ", "SPY"
]

if "demo_cash" not in st.session_state:
    st.session_state.demo_cash = STARTING_CASH

if "holding" not in st.session_state:
    st.session_state.holding = None

if "entry_price" not in st.session_state:
    st.session_state.entry_price = 0.0

if "invested_ils" not in st.session_state:
    st.session_state.invested_ils = 0.0

if "last_results" not in st.session_state:
    st.session_state.last_results = []


def analyze(ticker):
    data = yf.Ticker(ticker).history(period="6mo")

    if data.empty or len(data) < 50:
        return None

    close = data["Close"].dropna()

    if len(close) < 50:
        return None

    price = float(close.iloc[-1])
    ma20 = float(close.tail(20).mean())
    ma50 = float(close.tail(50).mean())
    change = (price / float(close.iloc[-20]) - 1) * 100

    score = 0

    if price > ma20:
        score += 1

    if ma20 > ma50:
        score += 1

    if change > 0:
        score += 1

    return {
        "מניה": ticker,
        "מחיר": price,
        "שינוי": change,
        "ממוצע20": ma20,
        "ממוצע50": ma50,
        "ציון": score,
    }


st.title("🤖 סוכן המסחר שלי")
st.success("✅ הסוכן פעיל — מצב דמו בלבד")

st.subheader("💰 תיק דמו")

c1, c2 = st.columns(2)
c1.metric("הון התחלתי", "₪10,000")
c2.metric("מצב", "דמו")

symbol = st.selectbox(
    "בחר מניה לבדיקה",
    STOCKS
)

if st.button("🔍 נתח את המניה"):
    try:
        item = analyze(symbol)

        if item is None:
            st.error("לא התקבלו מספיק נתוני שוק.")

        else:
            st.subheader("📊 תוצאות הניתוח")

            st.metric(
                "מחיר נוכחי",
                f'${item["מחיר"]:.2f}'
            )

            st.metric(
                "שינוי בתקופה",
                f'{item["שינוי"]:.2f}%'
            )

            st.write(
                f'ממוצע 20 יום: ${item["ממוצע20"]:.2f}'
            )

            st.write(
                f'ממוצע 50 יום: ${item["ממוצע50"]:.2f}'
            )

            if item["ציון"] == 3:
                st.success("🟢 החלטת הסוכן: מועמדת לקנייה")

            elif item["ציון"] == 2:
                st.warning("🟡 החלטת הס

import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="סוכן המסחר שלי",
    page_icon="🤖",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        direction: rtl;
    }
    h1, h2, h3, p {
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 סוכן המסחר שלי")
st.success("✅ הסוכן פעיל ומוכן לעבודה")

st.subheader("💰 תיק דמו")

col1, col2 = st.columns(2)

with col1:
    st.metric("הון התחלתי", "₪10,000")

with col2:
    st.metric("מצב", "דמו")

stocks = [
    "MSFT",
    "NVDA",
    "AAPL",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "QQQ",
    "SPY"
]

symbol = st.selectbox(
    "בחר מניה לבדיקה",
    stocks
)

if st.button("🔍 נתח את המניה"):
    try:
        data = yf.Ticker(symbol).history(period="6mo")

        if data.empty:
            st.error("לא התקבלו נתוני שוק")
        else:
            price = float(data["Close"].iloc[-1])

            ma20 = float(data["Close"].tail(20).mean())
            ma50 = float(data["Close"].tail(50).mean())

            change = (
                (price / float(data["Close"].iloc[-20])) - 1
            ) * 100

            score = 0

            if price > ma20:
                score += 1

            if ma20 > ma50:
                score += 1

            if change > 0:
                score += 1

            st.subheader("📊 תוצאות הניתוח")

            st.metric(
                "מחיר נוכחי",
                f"${price:.2f}"
            )

            st.metric(
                "שינוי בתקופה",
                f"{change:.2f}%"
            )

            st.write(f"ממוצע 20 יום: ${ma20:.2f}")
            st.write(f"ממוצע 50 יום: ${ma50:.2f}")

            if score == 3:
                st.success("🟢 החלטת הסוכן: מועמדת לקנייה")
                st.write("המגמה שנבדקה חיובית.")

            elif score == 2:
                st.warning("🟡 החלטת הסוכן: מעקב")
                st.write("יש סימנים חיוביים, אבל הסוכן ממתין.")

            else:
                st.error("🔴 החלטת הסוכן: לא לקנות כרגע")
                st.write("התנאים שנבדקו אינם מספיק חזקים.")

            st.info(
                "זהו סוכן דמו לצורכי בדיקה ולמידה בלבד. "
                "הוא אינו מבצע עסקאות בכסף אמיתי."
            )

    except Exception as e:
        st.error("אירעה שגיאה בקבלת נתוני השוק")
        st.write(str(e))

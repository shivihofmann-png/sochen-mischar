import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="סוכן המסחר",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 סוכן המסחר שלי")
st.caption("בדיקת נתוני שוק אמיתיים")

symbol = st.selectbox(
    "בחר נכס",
    ["MSFT", "NVDA", "AAPL", "AMZN", "GOOGL", "META", "TSLA", "QQQ", "SPY"]
)

if st.button("🔄 בדוק מחיר עכשיו", use_container_width=True):

    data = yf.download(
        symbol,
        period="1mo",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        st.error("לא התקבלו נתונים")
    else:
        price = float(data["Close"].iloc[-1])

        st.success("✅ הנת

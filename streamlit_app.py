import streamlit as st
import yfinance as yf
st.title("🤖 סוכן המסחר שלי")
     symbol = st.selectbox(
    "בחר מניה",
    ["MSFT", "NVDA", "AAPL", "AMZN", "GOOGL", "META", "TSLA", "QQQ", "SPY"]
)

if st.button("בדוק מחיר עדכני"):
    data = yf.Ticker(symbol).history(period="5d")

    if data.empty:
        st.error("לא התקבלו נתוני שוק")
    else:
        price = float(data["Close"].iloc[-1])
        st.metric("מחיר עדכני", f"${price:,.2f}")
        

import streamlit as st
import yfinance as yf

st.title("Trading Agent")
st.success("App is working")
symbol = st.selectbox(
    "Choose stock",
    ["MSFT", "NVDA", "AAPL", "AMZN", "GOOGL", "META", "TSLA", "QQQ", "SPY"]
)

if st.button("Check real price"):
    data = yf.Ticker(symbol).history(period="5d")

    if data.empty:
        st.error("No market data received")
    else:
        price = float(data["Close"].iloc[-1])
        st.metric("Latest price", f"${price:,.2f}")

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="סוכן המסחר שלי",
    page_icon="🤖",
    layout="centered"
)

STARTING_CASH = 10000.0

ASSETS = {
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "AAPL": "Apple",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet",
    "META": "Meta",
    "TSLA": "Tesla",
    "QQQ": "Nasdaq 100 ETF",
    "SPY": "S&P 500 ETF"
}

if "cash" not in st.session_state:
    st.session_state.cash = STARTING_CASH

@st.cache_data(ttl=900)
def get_market_data(symbol):
    data = yf.download(
        symbol,
        period="6mo",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty or len(data) < 30:
        return None

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    close = close.dropna()

    if len(close) < 30:
        return None

    price = float(close.iloc[-1])
    ma20 = float(close.tail(20).mean())
    ma50 = float(close.tail(50).mean()) if len(close) >= 50 else ma20

    return_20 = (
        (price / float(close.iloc[-21]) - 1) * 100
        if len(close) >= 21
        else 0
    )

    return_60 = (
        (price / float(close.iloc[-61]) - 1) * 100
        if len(close) >= 61
        else return_20
    )

    volatility = float(
        close.pct_change().tail(20).std() * 100
    )

    return {
        "price": price,
        "ma20": ma20,
        "ma50": ma50,
        "return20": return_20,
        "return60": return_60,
        "vol

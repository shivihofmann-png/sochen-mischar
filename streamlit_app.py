import streamlit as st
import yfinance as yf
import json
import os

STATE_FILE = "portfolio.json"

st.set_page_config(
    page_title="סוכן השקעות",
    page_icon="📈",
    layout="centered"
)

st.title("📈 סוכן ההשקעות")
st.caption("תיק דמו אוטומטי")

def load_portfolio():
    if not os.path.exists(STATE_FILE):
        return {
            "cash": 10000.0,
            "positions": {},
            "trades": []
        }

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_usd_ils_rate():
    data = yf.download(
        "ILS=X",
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        return 1.0

    return float(data["Close"].squeeze().iloc[-1])

def get_price_ils(symbol, usd_ils):
    data = yf.download(
        symbol,
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        return None

    price_usd = float(data["Close"].squeeze().iloc[-1])
    return price_usd * usd_ils

state = load_portfolio()
usd_ils = get_usd_ils_rate()

cash = float(state.get("cash", 0))
positions = state.get("positions", {})
trades = state.get("trades", [])

positions_value = 0.0
rows = []

for symbol, position in positions.items():
    shares = position.get("shares", 0)
    buy_price = float(position.get("buy_price", 0))

    current_price = get_price_ils(symbol, usd_ils)

    if current_price is None:
        current_price = buy_price

    current_value = shares * current_price
    invested = shares * buy_price
    profit = current_value - invested
    profit_pct = (profit / invested * 100) if invested > 0 else 0

    positions_value += current_value

    rows.append({
        "מניה": symbol,
        "כמות": shares,
        "מחיר קנייה ₪": round(buy_price, 2),
        "מחיר נוכחי ₪": round(current_price, 2),
        "שווי ₪": round(current_value, 2),
        "רווח/הפסד ₪": round(profit, 2),
        "רווח/הפסד %": round(profit_pct, 2)
    })

total_value = cash + positions_value
profit_total = total_value - 10000
profit_pct_total = (profit_total / 10000) * 100
excess = max(0, total_value - 50000)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💰 שווי התיק",
        f"₪{total_value:,.2f}",
        f"{profit_total:+,.2f} ₪"
    )

with col2:
    st.metric(
        "💵 מזומן",
        f"₪{cash:,.2f}"
    )

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "📊 תשואה",
        f"{profit_pct_total:+.2f}%"
    )

with col4:
    st.metric(
        "🏦 עודף מעל ₪50,000",
        f"₪{excess:,.2f}"
    )

st.divider()

st.subheader("📌 פוזיציות פתוחות")

if rows:
    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("אין כרגע מניות בתיק")

st.divider()

st.subheader("📒 יומן עסקאות")

if trades:
    trade_rows = []

    for trade in reversed(trades):
        trade_rows.append({
            "זמן": trade.get("date", ""),
            "פעולה": trade.get("action", ""),
            "מניה": trade.get("symbol", ""),
            "כמות": trade.get("shares", ""),
            "מחיר ₪": trade.get("price", ""),
            "סכום ₪": trade.get("value", "")
        })

    st.dataframe(
        trade_rows,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("אין עדיין עסקאות")

st.divider()

st.caption(
    f"שער דולר/שקל שנעשה בו שימוש: {usd_ils:.4f}"
)

st.caption(
    "האפליקציה היא למסך צפייה בלבד. העסקאות מתבצעות כרגע רק בתיק הדמו של הסוכן."
)

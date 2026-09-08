import streamlit as st
import yfinance as yf
from datetime import datetime, timezone, timedelta
st.set_page_config(
    page_title="סוכן המסחר שלי",
    page_icon="🤖"
)

st.title("🤖 סוכן המסחר שלי")
st.success("✅ הסוכן פעיל")

st.metric(
    "תיק דמו",
    "₪10,000"
)

stocks = [
    "MSFT",
    "NVDA",
    "AAPL",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "QQQ",
    "SPY",
    "AMD",
    "AVGO",
    "NFLX",
    "CRM",
    "ORCL",
    "PLTR",
    "UBER",
    "JPM",
    "V",
    "MA",
    "COST",
    "WMT",
    "LLY",
    "XOM",
    "BA",
    "DIS",
]

if st.button("🚀 סרוק את כל המניות"):

    results = []

    for ticker in stocks:

        data = yf.Ticker(ticker).history(
            period="6mo"
        )

        if len(data) >= 61:

            close = data["Close"]

            price = float(close.iloc[-1])
            ma20 = float(close.tail(20).mean())
            ma50 = float(close.tail(50).mean())

            mom20 = (
                price / float(close.iloc[-21]) - 1
            ) * 100

            mom60 = (
                price / float(close.iloc[-61]) - 1
            ) * 100

            vol = float(
                close.pct_change()
                .tail(20)
                .std()
                * 100
            )

            score = 50.0

            if price > ma20:
                score += 12
            else:
                score -= 12

            if ma20 > ma50:
                score += 12
            else:
                score -= 8

            score += max(
                -15,
                min(
                    15,
                    mom20 * 0.7
                )
            )

            score += max(
                -10,
                min(
                    10,
                    mom60 * 0.25
                )
            )

            if vol < 2:
                score += 4

            if vol > 5:
                score -= 8

            score = max(
                0,
                min(
                    100,
                    score
                )
            )

            results.append(
                (
                    ticker,
                    price,
                    mom20,
                    mom60,
                    vol,
                    round(score, 1)
                )
            )

    results.sort(
        key=lambda x: x[5],
        reverse=True
    )

    st.subheader(
        "🏆 דירוג הסוכן"
    )

    for i, item in enumerate(
        results,
        start=1
    ):

        st.write(
            f"{i}. {item[0]} | "
            f"ציון {item[5]}/100 | "
            f"${item[1]:.2f}"
        )

    if results:

        winner = results[0]

        st.success(
            f"🏆 המובילה כרגע: "
            f"{winner[0]} "
            f"עם ציון "
            f"{winner[5]}/100"
        )
if "winner" in locals():
    if winner[5] >= 80:
        st.success("🟢 החלטת הסוכן: מועמדת חזקה")
    elif winner[5] >= 70:
        st.warning("🟡 החלטת הסוכן: מעקב")
    else:
        st.error("🔴 החלטת הסוכן: לא לפעול כרגע")
    "⚠️ דמו בלבד — אין מסחר בכסף אמיתי"

st.divider()
st.subheader("💰 תיק דמו")

if "cash" not in st.session_state:
    st.session_state.cash = 10000.0

if "holding" not in st.session_state:
    st.session_state.holding = None

if "entry_price" not in st.session_state:
    st.session_state.entry_price = 0.0

if "invested" not in st.session_state:
    st.session_state.invested = 0.0
    

if "trade_log" not in st.session_state:
    st.session_state.trade_log = []

if "winner" in locals() and winner[5] >= 80 and st.session_state.holding is None:
    amount = st.session_state.cash * 0.30
    st.session_state.trade_log.append({
    "מניה": winner[0],
    "מחיר קנייה": winner[1],
    "סכום": amount,
    "ציון": winner[5],
      "זמן קנייה": datetime.now(timezone(timedelta(hours=3))).strftime("%d/%m/%Y %H:%M")  
})
    st.session_state.cash -= amount
    st.session_state.holding = winner[0]
    st.session_state.entry_price = winner[1]
    st.session_state.invested = amount

    st.success(
        f"🟢 קנייה וירטואלית: {winner[0]} בסכום ₪{amount:,.2f}"
    )

current_value = 0.0
trade_profit = 0.0

if st.session_state.holding is not None:
    current_data = yf.Ticker(
        st.session_state.holding
    ).history(period="1d")

    if not current_data.empty:
        current_price = float(current_data["Close"].iloc[-1])

        current_value = (
            st.session_state.invested
            * current_price
            / st.session_state.entry_price
        )

        trade_profit = (
            current_value
            - st.session_state.invested
        )
    else:
        current_value = st.session_state.invested
trade_return = (
    (current_value / st.session_state.invested - 1) * 100
    if st.session_state.invested > 0
    else 0.0
)
total_value = st.session_state.cash + current_value
profit = total_value - 10000.0
target_value = 50000.0
excess = max(0.0, total_value - target_value)
st.metric("תשואה בעסקה", f"{trade_return:.2f}%")
st.metric("שווי תיק", f"₪{total_value:,.2f}")
st.metric("מזומן", f"₪{st.session_state.cash:,.2f}")
st.metric("רווח / הפסד", f"₪{profit:,.2f}")
st.metric("רווח / הפסד בעסקה", f"₪{trade_profit:,.2f}")
st.metric("עודף מעל 50,000 ₪", f"₪{excess:,.2f}")
st.write(
f"📌 מחזיק כרגע: {st.session_state.holding}"
    )
if st.session_state.holding is not None:
    if st.button("🔴 מכור עכשיו"):
        sale_value = current_value
        sale_profit = sale_value - st.session_state.invested

        st.session_state.cash += sale_value

        st.session_state.trade_log.append({
            "מניה": st.session_state.holding,
            "מחיר מכירה": current_price,
            "סכום": sale_value,
            "רווח / הפסד": sale_profit,
            "פעולה": "מכירה"
        })

        st.session_state.holding = None
        st.session_state.entry_price = 0.0
        st.session_state.invested = 0.0

        st.rerun()
st.divider()
st.subheader("📒 יומן עסקאות")

if st.session_state.trade_log:
    st.dataframe(
        st.session_state.trade_log,
        use_container_width=True
    )
else:
    st.info("עדיין אין עסקאות ביומן")

import streamlit as st
import yfinance as yf

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
    "SPY"
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

st.caption(
    "⚠️ דמו בלבד — אין מסחר בכסף אמיתי"
)

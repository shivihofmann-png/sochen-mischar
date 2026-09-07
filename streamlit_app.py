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
            period="3mo"
        )

        if len(data) >= 20:

            close = data["Close"]

            price = float(
                close.iloc[-1]
            )

            old_price = float(
                close.iloc[-20]
            )

            change = (
                price / old_price - 1
            ) * 100

            results.append(
                (
                    ticker,
                    price,
                    change
                )
            )

    results.sort(
        key=lambda x: x[2],
        reverse=True
    )

    st.subheader(
        "🏆 דירוג לפי מומנטום"
    )

    for i, item in enumerate(
        results,
        start=1
    ):

        ticker = item[0]
        price = item[1]
        change = item[2]

        st.write(
            f"{i}. {ticker} | "
            f"${price:.2f} | "
            f"{change:.2f}%"
        )

    if results:

        winner = results[0]

        st.success(
            f"🏆 המובילה כרגע: "
            f"{winner[0]}"
        )

st.caption(
    "⚠️ דמו בלבד — אין מסחר בכסף אמיתי"
)

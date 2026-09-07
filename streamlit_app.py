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
st.divider()
st.subheader("🤖 סריקה אוטומטית")

if st.button("🚀 סרוק את כל המניות"):
    results = []

    with st.spinner("הסוכן סורק את השוק..."):
        for ticker in stocks:
            try:
                data = yf.Ticker(ticker).history(period="6mo")

                if len(data) >= 50:
                    close = data["Close"]
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

                    results.append(
                        {
                            "מניה": ticker,
                            "מחיר": round(price, 2),
                            "שינוי %": round(change, 2),
                            "ציון": score
                        }
                    )

            except Exception:
                pass

    results = sorted(
        results,
        key=lambda x: x["ציון"],
        reverse=True
    )
st.session_state.last_results = results
    if results:
        st.subheader("🏆 דירוג הסוכן")

        for i, item in enumerate(results, start=1):
            st.write(
                f'{i}. {item["מניה"]} | '
                f'ציון {item["ציון"]}/3 | '
                f'${item["מחיר"]} | '
                f'{item["שינוי %"]}%'
            )

        winner = results[0]

        st.success(
            f'🏆 המועמד המוביל: {winner["מניה"]} '
            f'עם ציון {winner["ציון"]}/3'
        )
    else:
        st.error("לא התקבלו מספיק נתונים לסריקה")
st.divider()
st.subheader("💰 תיק דמו אוטונומי")

if "demo_cash" not in st.session_state:
    st.session_state.demo_cash = 10000.0

if "demo_holding" not in st.session_state:
    st.session_state.demo_holding = None

if "demo_entry_price" not in st.session_state:
    st.session_state.demo_entry_price = 0.0

if "demo_amount" not in st.session_state:
    st.session_state.demo_amount = 0.0

if "last_results" in st.session_state and st.session_state.last_results:
    winner = st.session_state.last_results[0]

    if st.session_state.demo_holding is None:
        if winner["ציון"] == 3:
            investment = st.session_state.demo_cash * 0.30
            st.session_state.demo_cash -= investment
            st.session_state.demo_holding = winner["מניה"]
            st.session_state.demo_entry_price = winner["מחיר"]
            st.session_state.demo_amount = investment

            st.success(
                f'🟢 קנייה וירטואלית: {winner["מניה"]}'
            )

    current_value = st.session_state.demo_amount

    if st.session_state.demo_holding:
        for item in st.session_state.last_results:
            if item["מניה"] == st.session_state.demo_holding:
                current_value = (
                    st.session_state.demo_amount
                    * item["מחיר"]
                    / st.session_state.demo_entry_price
                )

    total_value = (
        st.session_state.demo_cash
        + current_value
    )

    profit = total_value - 10000.0

    st.metric(
        "שווי תיק",
        f"₪{total_value:,.2f}"
    )

    st.metric(
        "מזומן",
        f"₪{st.session_state.demo_cash:,.2f}"
    )

    st.metric(
        "רווח / הפסד",
        f"₪{profit:,.2f}"
    )

    if st.session_state.demo_holding:
        st.write(
            f"📌 מחזיק כרגע: "
            f"{st.session_state.demo_holding}"
        )
else:
    st.info(
        "בצע קודם סריקה אוטומטית "
        "כדי שהסוכן יוכל לבחור נכס."
    )

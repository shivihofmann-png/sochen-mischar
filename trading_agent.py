import json
import os
from datetime import datetime

import yfinance as yf

STARTING_CASH = 10_000.0

# מניות שהסוכן יבדוק בשלב הניסוי
SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
    "META", "TSLA", "AMD", "AVGO", "NFLX",
    "JPM", "V", "COST", "WMT", "LLY"
]

STATE_FILE = "portfolio.json"

# ניהול סיכון
MAX_POSITION_PCT = 0.15      # עד 15% מהתיק בפוזיציה אחת
MAX_POSITIONS = 6            # עד 6 מניות במקביל
def get_usd_ils_rate():
    data = yf.download(
        "ILS=X",
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        raise Exception("Could not get USD/ILS rate")

    return float(data["Close"].squeeze().iloc[-1])

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return {
        "cash": STARTING_CASH,
        "positions": {},
        "trades": []
    }


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_data(symbol):
    data = yf.download(
            symbol,
        period="60mo",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty or len(data) < 50:
        return None
    close = data["Close"].squeeze()
    usd_ils = get_usd_ils_rate()

    price = float(close.iloc[-1]) * usd_ils
    ma20 = float(close.rolling(20).mean().iloc[-1]) * usd_ils
    ma50 = float(close.rolling(50).mean().iloc[-1]) * usd_ils

    return price, ma20, ma50


def portfolio_value(state, prices):
    total = state["cash"]

    for symbol, position in state["positions"].items():
        price = prices.get(symbol, position["buy_price"])
        total += position["shares"] * price

    return total


def main():
    state = load_state()
    prices = {}
    signals = {}

    print("=== TRADING AGENT START ===")
    print("Time:", datetime.now().isoformat())

    # בדיקת השוק
    for symbol in SYMBOLS:
        try:
            result = get_data(symbol)

            if result is None:
                continue

            price, ma20, ma50 = result
            prices[symbol] = price

            # אות פשוט למגמה חיובית
            signals[symbol] = price > ma20 > ma50

        except Exception as e:
            print(f"Could not read {symbol}: {e}")

    total_value = portfolio_value(state, prices)

    # מכירה אם המגמה נשברת
    for symbol in list(state["positions"].keys()):
        if symbol not in prices:
            continue

        price = prices[symbol]
        position = state["positions"][symbol]

        try:
            result = get_data(symbol)
            if result is None:
                continue

            _, ma20, ma50 = result

            if price < ma20 or ma20 < ma50:
                shares = position["shares"]
                proceeds = shares * price

                state["cash"] += proceeds

                state["trades"].append({
                    "date": datetime.now().isoformat(),
                    "action": "SELL",
                    "symbol": symbol,
                    "shares": shares,
                    "price": round(price, 2),
                    "value": round(proceeds, 2)
                })

                del state["positions"][symbol]

                print(
                    f"SELL {shares} shares of {symbol} "
                    f"@ {price:.2f}"
                )

        except Exception as e:
            print(f"Sell check failed for {symbol}: {e}")

    # חישוב מחדש לאחר מכירות
    total_value = portfolio_value(state, prices)

    # קנייה לפי תקציב, לא לפי "מניה אחת"
    candidates = [
        symbol for symbol, signal in signals.items()
        if signal and symbol not in state["positions"]
    ]

    for symbol in candidates:
        if len(state["positions"]) >= MAX_POSITIONS:
            break

        price = prices[symbol]

        # עד 15% משווי התיק לעסקה
        position_budget = total_value * MAX_POSITION_PCT
        position_budget = min(position_budget, state["cash"])

        shares = int(position_budget // price)

        if shares < 1:
            continue

        cost = shares * price

        state["cash"] -= cost

        state["positions"][symbol] = {
            "shares": shares,
            "buy_price": round(price, 2),
            "buy_date": datetime.now().isoformat()
        }

        state["trades"].append({
            "date": datetime.now().isoformat(),
            "action": "BUY",
            "symbol": symbol,
            "shares": shares,
            "price": round(price, 2),
            "value": round(cost, 2)
        })

        print(
            f"BUY {shares} shares of {symbol} "
            f"@ {price:.2f} | Cost: {cost:.2f}"
        )

    total_value = portfolio_value(state, prices)

    print()
    print("Cash:", round(state["cash"], 2))
    print("Positions:", state["positions"])
    print("Portfolio value:", round(total_value, 2))
    print("=== TRADING AGENT END ===")

    save_state(state)


if __name__ == "__main__":
    main()

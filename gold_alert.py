import json
import os
import re
import time
import requests

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

GOLD_URL = "https://stooq.com/q/l/?s=xauusd"
FX_URL = "https://open.er-api.com/v6/latest/USD"

IMPORT_DUTY = 5
GST = 3
LOCAL_PREMIUM = 250
CALIBRATION = 0.9828

STATE_FILE = "state.json"

GET_UPDATES_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
SEND_MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_update_id": 0,
        "last_auto_alert_hour": -1
    }


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(GOLD_URL, headers=headers, timeout=20)
    r.raise_for_status()

    match = re.search(r"\d+\.\d+", r.text)
    if not match:
        raise Exception("Gold price not found")

    return float(match.group())


def get_usdinr():
    r = requests.get(FX_URL, timeout=20)
    r.raise_for_status()
    return float(r.json()["rates"]["INR"])


def get_rates():
    usd_gold = get_gold_price()
    usd_inr = get_usdinr()

    gram_price = (usd_gold * usd_inr) / 31.103
    price_10g = gram_price * 10

    price_10g = price_10g * (1 + IMPORT_DUTY / 100)
    price_10g = price_10g * (1 + GST / 100)
    price_10g = price_10g + LOCAL_PREMIUM
    price_10g = price_10g * CALIBRATION

    price_22k = price_10g * (22 / 24)

    return round(price_10g), round(price_22k), usd_gold, usd_inr


def send_telegram(chat_id, msg):
    payload = {
        "chat_id": chat_id,
        "text": msg
    }
    r = requests.post(SEND_MESSAGE_URL, data=payload, timeout=20)
    r.raise_for_status()


def build_message(title, price_24k, price_22k, usd_gold, usd_inr):
    return f"""{title} 🇮🇳

24K: ₹{price_24k:,} / 10g
22K: ₹{price_22k:,} / 10g

USD Gold: ${usd_gold:.2f} / ounce
USDINR: {usd_inr:.2f}
"""


def handle_commands(state, price_24k, price_22k, usd_gold, usd_inr):
    offset = state.get("last_update_id", 0) + 1

    r = requests.get(GET_UPDATES_URL, params={"offset": offset}, timeout=20)
    r.raise_for_status()
    data = r.json()

    if not data.get("ok"):
        return state

    for item in data.get("result", []):
        update_id = item.get("update_id", 0)
        message = item.get("message", {})
        text = message.get("text", "")
        chat_id = str(message.get("chat", {}).get("id", ""))

        if update_id > state.get("last_update_id", 0):
            state["last_update_id"] = update_id

        if not text or not chat_id:
            continue

        cmd = text.strip().lower()

        if cmd in ["price", "/price"]:
            reply = build_message("Gold Price", price_24k, price_22k, usd_gold, usd_inr)
            send_telegram(chat_id, reply)

        elif cmd == "24k":
            send_telegram(chat_id, f"24K Gold: ₹{price_24k:,} / 10g")

        elif cmd == "22k":
            send_telegram(chat_id, f"22K Gold: ₹{price_22k:,} / 10g")

        elif cmd == "help":
            send_telegram(chat_id, "Commands:\nprice\n24k\n22k\nhelp")

    return state


def handle_auto_alert(state, price_24k, price_22k, usd_gold, usd_inr):
    current_hour = int(time.time() // 3600)

    if current_hour % 2 == 0 and state.get("last_auto_alert_hour") != current_hour:
        msg = build_message("Gold Alert India", price_24k, price_22k, usd_gold, usd_inr)
        send_telegram(CHAT_ID, msg)
        state["last_auto_alert_hour"] = current_hour

    return state


def main():
    state = load_state()

    price_24k, price_22k, usd_gold, usd_inr = get_rates()

    state = handle_commands(state, price_24k, price_22k, usd_gold, usd_inr)
    state = handle_auto_alert(state, price_24k, price_22k, usd_gold, usd_inr)

    save_state(state)


if __name__ == "__main__":
    main()

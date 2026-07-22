import json
import os
import time
import requests

# ⚠️ OLD TOKEN (as you said)
BOT_TOKEN = "8681012084:AAFJMsY1cFROKLKADDOvAPNd88cunYhSci8"
CHANNEL_CHAT_ID = "-1003580840383"

# ✅ 100% Free, Bot-Friendly and Fast API (No Key Required)
GOLD_URL = "https://api.gold-api.com/price/XAU"
FX_URL = "https://open.er-api.com/v6/latest/USD"

IMPORT_DUTY = 5
GST = 3
LOCAL_PREMIUM = 250
CALIBRATION = 0.9828

STATE_FILE = "state.json"
SEND_MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "last_auto_alert_hour": -1
    }


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


def get_gold_price():
    headers = {
        "User-Agent": "GoldAlertBot/1.0"
    }
    r = requests.get(GOLD_URL, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()
    
    # Gold-API सीधा JSON में "price" फील्ड देता है
    if "price" in data:
        return float(data["price"])
    else:
        raise ValueError("Gold price field 'price' not found in JSON response")


def get_usdinr():
    r = requests.get(FX_URL, timeout=20)
    r.raise_for_status()
    data = r.json()
    return float(data["rates"]["INR"])


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


def send_telegram(msg):
    payload = {
        "chat_id": CHANNEL_CHAT_ID,
        "text": msg
    }
    r = requests.post(SEND_MESSAGE_URL, data=payload, timeout=20)
    print("Status:", r.status_code)
    print("Response:", r.text)
    r.raise_for_status()


def build_message(price_24k, price_22k, usd_gold, usd_inr):
    return f"""Gold Alert India 🇮🇳

24K: ₹{price_24k:,} / 10g
22K: ₹{price_22k:,} / 10g
USD Gold: ${usd_gold:.2f} / ounce
USDINR: {usd_inr:.2f}
"""


def handle_auto_alert(state, price_24k, price_22k, usd_gold, usd_inr):
    current_hour = int(time.time() // 3600)
    # हर 2 घंटे में 1 बार
    if

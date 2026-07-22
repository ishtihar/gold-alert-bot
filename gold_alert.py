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
        "last_auto_alert_hour": -

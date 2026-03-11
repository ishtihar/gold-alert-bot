import re
import requests

# ===== TELEGRAM =====
BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

# ===== SOURCES =====
GOLD_URL = "https://stooq.com/q/l/?s=xauusd"
FX_URL = "https://open.er-api.com/v6/latest/USD"

# ===== INDIA TAX =====
IMPORT_DUTY = 6.0
GST = 3.0


def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(GOLD_URL, headers=headers)
    r.raise_for_status()

    match = re.search(r"\d+\.\d+", r.text)
    if not match:
        raise Exception("Gold price not found")

    return float(match.group())


def get_usd_inr():
    r = requests.get(FX_URL)
    r.raise_for_status()

    data = r.json()
    return data["rates"]["INR"]


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=payload)


def main():

    usd_gold = get_gold_price()
    usd_inr = get_usd_inr()

    gram_price = (usd_gold * usd_inr) / 31.103

    price_10g = gram_price * 10

    # import duty
    price_10g = price_10g * (1 + IMPORT_DUTY / 100)

    # GST
    price_10g = price_10g * (1 + GST / 100)

    price_22k = price_10g * (22 / 24)

    message = f"""
Gold Alert India 🇮🇳

24K: ₹{price_10g:.2f} / 10g
22K: ₹{price_22k:.2f} / 10g

USD Gold: ${usd_gold:.2f} / ounce
USDINR: {usd_inr:.2f}
"""

    send_telegram(message)


if __name__ == "__main__":
    main()

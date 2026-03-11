import requests
import json
import os

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

PRICE_FILE = "last_price.json"


def get_gold_price():

    gold_url = "https://api.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": "goldapi-demo"}

    r = requests.get(gold_url, headers=headers)
    data = r.json()

    usd_ounce = data["price"]

    # USDINR
    fx = requests.get("https://open.er-api.com/v6/latest/USD").json()
    usdinr = fx["rates"]["INR"]

    # convert
    inr_ounce = usd_ounce * usdinr
    gram_24k = inr_ounce / 31.1035

    # GST + import adjustment
    gram_24k = gram_24k * 1.10

    price_10g = gram_24k * 10
    price_22k = price_10g * 0.916

    return round(price_10g), round(price_22k), usd_ounce, usdinr


def load_last_price():
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE) as f:
            return json.load(f)
    return None


def save_price(price):
    with open(PRICE_FILE, "w") as f:
        json.dump(price, f)


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=payload)


def main():

    price_24k, price_22k, usd_gold, usdinr = get_gold_price()

    last = load_last_price()

    if last is None or last["24k"] != price_24k:

        message = f"""
Gold Alert India 🇮🇳

24K: ₹{price_24k} / 10g
22K: ₹{price_22k} / 10g

USD Gold: ${usd_gold}
USDINR: {usdinr}
"""

        send_message(message)

        save_price({
            "24k": price_24k
        })


if __name__ == "__main__":
    main()

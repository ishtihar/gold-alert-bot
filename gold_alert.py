import requests
import json
import os

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

PRICE_FILE = "last_price.json"


def get_gold_price():

    # Gold price USD per ounce
    gold = requests.get("https://api.metals.live/v1/spot/gold").json()
    usd_ounce = gold[0]["price"]

    # USDINR
    fx = requests.get("https://open.er-api.com/v6/latest/USD").json()
    usdinr = fx["rates"]["INR"]

    # convert to INR
    inr_ounce = usd_ounce * usdinr

    gram_price = inr_ounce / 31.1035

    # import duty + GST adjustment
    gram_price = gram_price * 1.10

    price_24k_10g = gram_price * 10
    price_22k_10g = price_24k_10g * 0.916

    return round(price_24k_10g), round(price_22k_10g), usd_ounce, usdinr


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

    price24, price22, usd_gold, usdinr = get_gold_price()

    last = load_last_price()

    if last is None or last["price"] != price24:

        message = f"""
Gold Alert India 🇮🇳

24K: ₹{price24} / 10g
22K: ₹{price22} / 10g

USD Gold: ${usd_gold}
USDINR: {usdinr}
"""

        send_message(message)

        save_price({"price": price24})


if __name__ == "__main__":
    main()

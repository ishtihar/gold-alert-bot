import requests

# Tumhara bot token aur chat id
BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "649507132"

def get_gold_price():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url)
    data = r.json()

    # API se price nikalna
    price = data[0]['price']
    return price


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=payload)


price = get_gold_price()

message = f"Gold price now: ${price} per ounce"

send_telegram(message)

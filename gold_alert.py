import requests

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "649507132"

def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": "goldapi-demo",
        "Content-Type": "application/json"
    }

    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()

    return data["price"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    r = requests.post(url, data=payload, timeout=20)
    r.raise_for_status()

def main():
    price = get_gold_price()
    message = f"Gold price now: ${price} per ounce"
    send_telegram(message)

if __name__ == "__main__":
    main()

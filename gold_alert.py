import requests
import re
from bs4 import BeautifulSoup

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

URL = "https://stooq.com/q/l/?s=xauusd"


def get_gold_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    match = re.search(r"\d+\.\d+", text)

    if not match:
        raise ValueError("Gold price not found")

    return float(match.group())


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=payload)


def main():
    price = get_gold_price()

    message = f"Gold price now: ${price} per ounce"

    send_telegram(message)


if __name__ == "__main__":
    main()

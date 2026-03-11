import requests
import re

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

GOLD_URL = "https://stooq.com/q/l/?s=xauusd"
FX_URL = "https://open.er-api.com/v6/latest/USD"


def get_gold_price_usd_per_ounce():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(GOLD_URL, headers=headers, timeout=20)
    r.raise_for_status()

    text = r.text
    match = re.search(r"\d+\.\d+", text)
    if not match:
        raise ValueError("Gold price not found")

    return float(match.group())


def get_usd_inr():
    r = requests.get(FX_URL, timeout=20)
    r.raise_for_status()
    data = r.json()

    if "rates" not in data or "INR" not in data["rates"]:
        raise ValueError("USD/INR rate not found")

    return float(data["rates"]["INR"])


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    r = requests.post(url, data=payload, timeout=20)
    r.raise_for_status()


def main():
    usd_per_ounce = get_gold_price_usd_per_ounce()
    usd_inr = get_usd_inr()

    # 1 troy ounce = 31.1034768 grams
    inr_per_gram_24k = (usd_per_ounce * usd_inr) / 31.1034768
    inr_per_10g_24k = inr_per_gram_24k * 10

    # 22K is approx 22/24 of 24K
    inr_per_gram_22k = inr_per_gram_24k * (22 / 24)
    inr_per_10g_22k = inr_per_gram_22k * 10

    message = (
        "Gold Alert India\n"
        f"24K: Rs {inr_per_gram_24k:.2f} per gram\n"
        f"24K: Rs {inr_per_10g_24k:.2f} per 10 gram\n"
        f"22K: Rs {inr_per_gram_22k:.2f} per gram\n"
        f"22K: Rs {inr_per_10g_22k:.2f} per 10 gram\n"
        f"USD Gold: ${usd_per_ounce:.2f} per ounce\n"
        f"USD/INR: {usd_inr:.2f}"
    )

    send_telegram(message)


if __name__ == "__main__":
    main()
    requests.post(url, data=payload)


def main():
    price = get_gold_price()

    message = f"Gold price now: ${price} per ounce"

    send_telegram(message)


if __name__ == "__main__":
    main()

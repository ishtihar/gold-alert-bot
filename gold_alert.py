import re
import requests

BOT_TOKEN = "8788695706:AAHVdIupcHwvsT-xVmH3mEEgTbpaQg6o0zU"
CHAT_ID = "5508496123"

# Gold spot source
GOLD_URL = "https://stooq.com/q/l/?s=xauusd"

# USD to INR source
FX_URL = "https://open.er-api.com/v6/latest/USD"

# India-side add-ons
IMPORT_DUTY_PERCENT = 6.0   # default based on current official budget change
GST_PERCENT = 3.0           # gold GST
LOCAL_PREMIUM_PER_10G = 0.0 # optional: add jeweller/city premium if you want, e.g. 500

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
    print("Telegram response:", r.text)
    r.raise_for_status()

def main():
    usd_per_ounce = get_gold_price_usd_per_ounce()
    usd_inr = get_usd_inr()

    # 1 troy ounce = 31.1034768 grams
    base_24k_per_gram = (usd_per_ounce * usd_inr) / 31.1034768
    base_24k_per_10g = base_24k_per_gram * 10

    # Add import duty
    after_duty_24k_per_10g = base_24k_per_10g * (1 + IMPORT_DUTY_PERCENT / 100)

    # Add any optional local premium
    before_gst_24k_per_10g = after_duty_24k_per_10g + LOCAL_PREMIUM_PER_10G

    # Add GST
    final_24k_per_10g = before_gst_24k_per_10g * (1 + GST_PERCENT / 100)

    # 22K approx from 24K purity ratio
    final_22k_per_10g = final_24k_per_10g * (22 / 24)

    # Also gram values
    final_24k_per_gram = final_24k_per_10g / 10
    final_22k_per_gram = final_22k_per_10g / 10

    message = (
        "Gold Alert India\n"
        f"24K: Rs {final_24k_per_gram:.2f} per gram\n"
        f"24K: Rs {final_24k_per_10g:.2f} per 10 gram\n"
        f"22K: Rs {final_22k_per_gram:.2f} per gram\n"
        f"22K: Rs {final_22k_per_10g:.2f} per 10 gram\n"
        "\n"
        f"Base Gold: ${usd_per_ounce:.2f} per ounce\n"
        f"USD/INR: {usd_inr:.2f}\n"
        f"Import Duty: {IMPORT_DUTY_PERCENT:.1f}%\n"
        f"GST: {GST_PERCENT:.1f}%\n"
        f"Local Premium: Rs {LOCAL_PREMIUM_PER_10G:.2f} per 10g"
    )

    print(message)
    send_telegram(message)

if __name__ == "__main__":
    main()    payload = {
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

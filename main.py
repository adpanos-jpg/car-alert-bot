import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime
import threading

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.car.gr/classifieds/cars/?make=hyundai,toyota,kia,honda,suzuki&year-from=2020&price-to=10000&mileage-to=60000"


def get_ads():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ads = soup.select("article")

    results = []
    for ad in ads[:10]:
        try:
            title = ad.get_text(strip=True)
            link = ad.find("a")["href"]
            results.append(f"{title}\nhttps://www.car.gr{link}")
        except:
            continue

    return results


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def job():
    print(f"[{datetime.now()}] Running daily car check...")

    try:
        ads = get_ads()

        if not ads:
            send_telegram("❌ Δεν βρέθηκαν αγγελίες σήμερα")
            return

        message = "🚗 Νέες αγγελίες:\n\n" + "\n\n".join(ads)
        send_telegram(message)

    except Exception as e:
        send_telegram(f"⚠️ Error στο bot: {e}")


def scheduler():
    while True:
        now = datetime.now()

        # 22:00 κάθε μέρα
        if now.hour == 22 and now.minute == 0:
            job()
            time.sleep(60)  # για να μην ξανατρέξει μέσα στο ίδιο λεπτό

        time.sleep(20)


if __name__ == "__main__":
    print("Bot started...")

    # τρέχει σε background thread
    t = threading.Thread(target=scheduler)
    t.start()

    # κρατάει το Railway service alive
    while True:
        time.sleep(3600)

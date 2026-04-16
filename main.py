import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.car.gr/classifieds/cars/?make=hyundai,toyota,kia,honda,suzuki&year-from=2022&price-to=10000&mileage-to=50000"

def get_ads():
    r = requests.get(URL)
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

def main():
    ads = get_ads()

    if not ads:
        send_telegram("❌ Δεν βρέθηκαν αγγελίες σήμερα")
        return

    message = "🚗 Νέες αγγελίες:\n\n" + "\n\n".join(ads)
    send_telegram(message)

if __name__ == "__main__":
    main()

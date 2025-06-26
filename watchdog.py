import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

WATCH_URL = os.getenv("BOT_URL")  # Сюда вставь ссылку на базар-бота, например: https://your-bazar-bot.onrender.com
TELEGRAM_TOKEN = os.getenv("WATCHDOG_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": ADMIN_ID, "text": message}
    requests.post(url, data=data)

def is_bot_alive():
    try:
        r = requests.get(WATCH_URL, timeout=10)
        return r.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🚀 Watchdog запущен. Следит за ботом...")
    while True:
        if not is_bot_alive():
            print("❌ Бот не отвечает. Отправляю тревогу...")
            send_alert("❗️ ВНИМАНИЕ: Базар-бот не отвечает!")
        else:
            print("✅ Бот работает нормально.")
        time.sleep(60 * 5)

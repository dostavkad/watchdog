import requests
import time
import os
from dotenv import load_dotenv
from threading import Thread
from flask import Flask, request

load_dotenv()

WATCH_URL = os.getenv("BOT_URL")
TELEGRAM_TOKEN = os.getenv("WATCHDOG_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

app = Flask(__name__)

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

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start" or text == "/status":
            if is_bot_alive():
                reply = "✅ Watchdog активен.\nОсновной бот: работает."
            else:
                reply = "⚠️ Watchdog работает, но основной бот НЕ отвечает!"
            send_alert(reply)
    return {"ok": True}

def watchdog_loop():
    print("🚀 Watchdog запущен. Следит за ботом...")
    while True:
        if not is_bot_alive():
            send_alert("❗️ ВНИМАНИЕ: Бот не отвечает!")
        else:
            print("✅ Бот работает нормально.")
        time.sleep(60 * 5)

if __name__ == "__main__":
    # Поток для постоянной проверки
    Thread(target=watchdog_loop).start()

    # Flask-сервер для обработки команд
    app.run(host="0.0.0.0"

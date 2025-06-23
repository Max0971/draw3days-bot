from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

# Отримуємо токен і шлях до вебхука
TOKEN = os.getenv("BOT_TOKEN") or "PASTE_YOUR_BOT_TOKEN_HERE"
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "webhook")
WEBHOOK_URL = f"https://draw3days-bot.onrender.com/{WEBHOOK_PATH}"

# Ініціалізація Flask та Telegram Application
app = Flask(__name__)
application = Application.builder().token(TOKEN).concurrent_updates(True).build()

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

# Додаємо обробник до Telegram Application
application.add_handler(CommandHandler("start", start))

# Головна сторінка (для перевірки)
@app.route("/", methods=["GET"])
def home():
    return "Бот працює! ✅", 200

# Обробник для Telegram Webhook
@app.route(f"/{WEBHOOK_PATH}", methods=["POST"])
def webhook():
    """Отримання Telegram update і передача до application."""
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, application.bot)
    asyncio.create_task(application.process_update(update))
    return "ok", 200

# Ініціалізація бота і встановлення вебхуку
async def setup_webhook():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.start()
    print(f"✅ Webhook встановлено: {WEBHOOK_URL}")

# Запуск Flask + Telegram Application
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(setup_webhook())

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

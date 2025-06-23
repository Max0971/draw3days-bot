from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")  # Заміни на токен напряму, якщо не хочеш використовувати середовище
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "webhook")  # Шлях до webhook, наприклад: "webhook"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

# Додаємо обробник
application.add_handler(CommandHandler("start", start))

# Головна сторінка (для перевірки в браузері)
@app.route("/", methods=["GET"])
def home():
    return "Бот працює! ✅", 200

# Webhook endpoint
@app.route(f"/{WEBHOOK_PATH}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok", 200

# Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    # Запуск Telegram-бота (без polling)
    asyncio.run(application.initialize())

    # Встановлення webhook (один раз після запуску)
    async def set_webhook():
        url = f"https://draw3days-bot.onrender.com/{WEBHOOK_PATH}"
        await application.bot.set_webhook(url)
        print(f"Webhook встановлено: {url}")

    asyncio.run(set_webhook())

    # Flask запускається як сервер
    app.run(host="0.0.0.0", port=port)

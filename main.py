import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder

# Налаштування логів
logging.basicConfig(level=logging.INFO)

# Flask сервер
flask_app = Flask(__name__)

# Токен з env
TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Створюємо Telegram Application
application = ApplicationBuilder().token("YOUR_TOKEN").pool_timeout(30).connect_timeout(30).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот, який працює через Render.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(context.error, telegram.error.TimedOut):
        await asyncio.sleep(5)
        await update.message.reply_text("Будь ласка, спробуйте ще раз")

# Додаємо хендлер
application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# Старт програми
if __name__ == "__main__":
    import asyncio

    async def run():
        webhook_url = f"https://{RENDER_EXTERNAL_HOSTNAME}/{TOKEN}"
        await application.bot.set_webhook(webhook_url)
        await application.initialize()
        await application.start()

    asyncio.run(run())

    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

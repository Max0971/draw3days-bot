import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Налаштування логів
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Токен з середовища Render
TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # автоматично підставляється Render'ом

# Flask ініціалізація
flask_app = Flask(__name__)

# Telegram Application
telegram_app = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я працюю як Telegram-бот через Render 🌐")

telegram_app.add_handler(CommandHandler("start", start))

# Webhook endpoint для Telegram
@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

# Головна точка входу
if __name__ == "__main__":
    import asyncio

    async def run():
        webhook_url = f"https://{RENDER_EXTERNAL_HOSTNAME}/{TOKEN}"
        logging.info(f"Встановлюємо webhook за адресою: {webhook_url}")
        await telegram_app.bot.set_webhook(webhook_url)
        await telegram_app.initialize()
        await telegram_app.start()

    asyncio.run(run())

    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

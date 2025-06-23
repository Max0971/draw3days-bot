from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN") or "YOUR_REAL_TOKEN"
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "webhook")
WEBHOOK_URL = f"https://draw3days-bot.onrender.com/{WEBHOOK_PATH}"

app = Flask(__name__)
application = Application.builder().token(TOKEN).concurrent_updates(True).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

application.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET"])
def home():
    return "Бот працює! ✅", 200

@app.route(f"/{WEBHOOK_PATH}", methods=["POST"])
def webhook():
    """Обробка вебхуку (викликає асинхронну функцію у фоновому режимі)."""
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, application.bot)
    asyncio.create_task(application.process_update(update))
    return "ok", 200

async def setup_webhook():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook встановлено: {WEBHOOK_URL}")
    await application.start()  # потрібен для коректної роботи webhook
    # application.run_polling() не викликаємо, бо ми використовуємо webhook

# Піднімаємо все разом
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(setup_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN") or "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "webhook")

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
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    url = f"https://draw3days-bot.onrender.com/{WEBHOOK_PATH}"

    async def main():
        await application.initialize()
        await application.bot.set_webhook(url)
        print(f"Webhook встановлено: {url}")

    asyncio.run(main())
    app.run(host="0.0.0.0", port=port)

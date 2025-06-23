from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")  # Переконайся, що в Render додано BOT_TOKEN

# Ініціалізація Flask
app = Flask(__name__)

# Ініціалізація Telegram Application
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я працюю.")

application.add_handler(CommandHandler("start", start))

# Flask endpoint для webhook
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Запуск Flask сервера
if __name__ == "__main__":
    import asyncio

    # Встановлюємо webhook
    async def main():
        await application.bot.set_webhook(f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
        print("Webhook встановлено")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()  # Не запускає polling, просто треба для start()

    asyncio.run(main())
    app.run(host="0.0.0.0", port=10000)  # Render запускає на 0.0.0.0

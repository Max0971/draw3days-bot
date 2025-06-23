from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = "ТУТ_ВАШ_ТОКЕН_БОТА"

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот працює!", 200

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

def run_bot():
    async def main():
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        await application.run_polling()  # Запускаємо бот (працює вічно)

    asyncio.run(main())

if __name__ == "__main__":
    # Запускаємо Telegram-бота у фоновому потоці
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    # Запускаємо Flask у головному потоці
    app.run(host="0.0.0.0", port=10000)

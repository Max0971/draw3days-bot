from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"

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

        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        await application.u
if __name__ == "__main__":
    # Запускаємо Telegram-бота у фоновому потоці
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    # Отримуємо порт з оточення (для Render)
    import os
    port = int(os.environ.get("PORT", 10000))

    # Запускаємо Flask у головному потоці
    app.run(host="0.0.0.0", port=port)

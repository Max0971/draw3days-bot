import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import Conflict
import os

TOKEN = "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"

# === Telegram bot logic ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    try:
        application.run_polling()
    except Conflict:
        print("⚠️ Бот вже запущений!")
    except Exception as e:
        print(f"Помилка: {e}")

# === Flask server for Render health check ===
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running", 200

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=10000)

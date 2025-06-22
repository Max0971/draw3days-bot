from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"

# Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

# Telegram handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

def run_bot():
    import asyncio
    async def main():
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        await application.run_polling()

    asyncio.run(main())

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)

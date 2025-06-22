from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import Conflict

TOKEN = "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    
    try:
        application.run_polling()
    except Conflict:
        print("⚠️ Бот вже запущений! Зупиніть інший екземпляр.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
from flask import Flask
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running", 200

if __name__ == '__main__':
    # Запускаємо Flask на порту 10000
    app.run(host='0.0.0.0', port=10000)

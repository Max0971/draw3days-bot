from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активний! ✅")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    application.run_polling()

if __name__ == "__main__":
    main()

from telegram.error import Conflict

try:
    app.run_polling()
except Conflict:
    print("⚠️ Бот вже запущений! Зупиніть інший екземпляр.")
except Exception as e:
    print(f"Помилка: {e}")

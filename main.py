import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Увімкнення логів
logging.basicConfig(level=logging.INFO)

# Токен бота
TOKEN = "7240793453:AAFu5f4ArOokx2knYlF8JLoSJFbc0tO8WvU"

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я працюю 🎉")

# Основна функція запуску
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Додаємо команду /start
    app.add_handler(CommandHandler("start", start))
    
    # Запускаємо бота
    app.run_polling()

if __name__ == "__main__":
    main()

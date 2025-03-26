import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Приклад даних: діалог та словниковий запас
daily_dialogue = (
    "A: Hi, how are you doing today?\n"
    "B: I'm doing well, thank you. How about you?\n"
    "A: Not too bad, just a bit busy with work.\n"
    "B: I understand. We all have those days.\n"
)

daily_vocabulary = [
    {
        "word": "meticulous",
        "definition": "showing great attention to detail; very careful and precise."
    },
    {
        "word": "resilient",
        "definition": "able to withstand or recover quickly from difficult conditions."
    },
]

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Вітаю! Я бот для вивчення англійської рівня B2.\n\n"
        "Доступні команди:\n"
        "/daily - отримати щоденну практику (діалог + слово дня)\n"
        "/vocab - переглянути нові слова\n"
        "/dialog - переглянути короткий діалог\n"
        "/quiz - перевірити свої знання (вікторина)"
    )
    await update.message.reply_text(welcome_text)

# Обробник команди /daily
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Ось твоя щоденна практика:\n\n"
    text += "Діалог:\n" + daily_dialogue + "\n"
    text += "Слово дня:\n"
    for vocab in daily_vocabulary:
        text += f"{vocab['word']}: {vocab['definition']}\n"
    await update.message.reply_text(text)

# Обробник команди /vocab
async def vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Сьогоднішні слова:\n"
    for vocab in daily_vocabulary:
        text += f"{vocab['word']}: {vocab['definition']}\n"
    await update.message.reply_text(text)

# Обробник команди /dialog
async def dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ось короткий діалог для практики:\n\n" + daily_dialogue)

# Обробник команди /quiz
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Яке слово означає 'able to withstand or recover quickly from difficult conditions'?"
    options = [
        InlineKeyboardButton("meticulous", callback_data='wrong'),
        InlineKeyboardButton("resilient", callback_data='correct')
    ]
    keyboard = InlineKeyboardMarkup.from_column(options)
    await update.message.reply_text(question, reply_markup=keyboard)

# Обробник кнопок для вікторини
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    answer = query.data
    if answer == 'correct':
        await query.edit_message_text(text="Правильно! Слово 'resilient' означає це.")
    else:
        await query.edit_message_text(text="Невірно. Спробуйте ще раз!")

def main():
    token = os.environ.get("TOKEN")
    if not token:
        logger.error("TOKEN не заданий. Будь ласка, встановіть змінну оточення TOKEN.")
        return

    application = Application.builder().token(token).build()

    # Реєстрація обробників команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("vocab", vocab))
    application.add_handler(CommandHandler("dialog", dialog))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота (полінг)
    application.run_polling()

if __name__ == '__main__':
    main()

import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# محیط وب برای زنده نگه داشتن
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# توکن رباتت رو اینجا بذار
TOKEN = '8000438969:AAFhj0ZEcVUehcY268sXcb26DUnCOiANlj8'

# شروع کار ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("لایسنس", callback_data='license')],
        [InlineKeyboardButton("کارت", callback_data='card')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('سلام! یکی از گزینه‌ها رو انتخاب کن:', reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "license":
        await query.edit_message_text(
            text="🔑 لایسنس خریداری شد ✅",
            reply_markup=main_menu_keyboard()
        )

    elif query.data == "card":
        await query.edit_message_text(
            text="💳 اطلاعات کارت:\nشماره کارت: 1234-5678-9012-3456",
            reply_markup=main_menu_keyboard()
        )

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("برگشت به منو اصلی", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def main():
    keep_alive()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(button_click))
    app_bot.run_polling()

if __name__ == '__main__':
    main()

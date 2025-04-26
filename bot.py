import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
import threading

# گرفتن توکن از محیط
BOT_TOKEN = os.environ["BOT_TOKEN"]

# تعریف ربات
app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()

# آیدی پشتیبانی
support_id = "@Unlock_mobile_com"

# دکمه‌های منوی اصلی
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📘 راهنما و سوالات پرتکرار", callback_data="faq")],
        [InlineKeyboardButton("📚 آموزش نصب و فعال‌سازی", url="https://xn--hgbk0gh11c.com/آموزش-آنلاک-گوشی-موبایل-بدون-حذف-اطلاع/")],
        [InlineKeyboardButton("💳 شرایط خرید لایسنس", callback_data="license")],
        [InlineKeyboardButton("💳 شماره کارت", callback_data="card")],
        [InlineKeyboardButton("🌐 سایت رسمی", url="https://xn--hgbk0gh11c.com/")],
        [InlineKeyboardButton("📩 پشتیبانی تلگرام", url="https://t.me/Unlock_mobile_com")]
    ]
    return InlineKeyboardMarkup(keyboard)

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 به ربات رسمی وب‌سایت آنلاک خوش آمدید!\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu_keyboard()
    )

# هندلر کلیک روی دکمه‌ها
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "faq":
        await query.edit_message_text(
            "💥 سوالات شما 💥\n"
            "🔹 چه مدل گوشی‌هایی رو میشه باز کرد؟ سامسونگ، شیائومی، هوآوی و ...\n"
            "🔹 نیاز به باکس؟ خیر\n"
            "🔹 ویندوز؟ ویندوز ۱۰ پرو\n"
            f"📩 پشتیبانی: {support_id}",
            reply_markup=main_menu_keyboard()
        )

    elif query.data == "license":
        await query.edit_message_text(
            "💳 شرایط خرید لایسنس:\n\n"
            "۱- مشاهده آموزش\n"
            "۲- پرداخت و ارسال رسید\n"
            "۳- ارسال Hardware ID\n"
            f"\n📩 پشتیبانی: {support_id}",
            reply_markup=main_menu_keyboard()
        )

    elif query.data == "card":
        await query.edit_message_text(
            "💳 شماره کارت:\n\n"
            "🔹 شماره کارت: ‎6104-3373-6006-3620‎\n"
            "🔹 بهزاد خزانی\n"
            "\nبعد از پرداخت اطلاعات رو به پشتیبانی بفرستید.",
            reply_markup=main_menu_keyboard()
        )

# ثبت فرمان‌ها
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CallbackQueryHandler(button_click))

# ---- سرور Flask برای باز کردن پورت ----
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app_flask.run(host="0.0.0.0", port=port)

# ---- اجرای ربات و Flask با هم ----
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    app_telegram.run_polling()

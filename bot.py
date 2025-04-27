import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

BOT_TOKEN   = os.environ["BOT_TOKEN"]
# آدرس دامنه‌ای که رندر یا رایلوِی بهت داده (بدون اسلش آخر)
DOMAIN      = os.environ["WEBHOOK_URL"]

# ----- کد ربات -----
app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

support_id = "@Unlock_mobile_com"
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📘 راهنما و سوالات پرتکرار", callback_data="faq")],
        [InlineKeyboardButton("📚 آموزش نصب و فعال‌سازی", url="https://…")],
        [InlineKeyboardButton("💳 شرایط خرید لایسنس", callback_data="license")],
        [InlineKeyboardButton("💳 شماره کارت", callback_data="card")],
        [InlineKeyboardButton("🌐 سایت رسمی", url="https://…")],
        [InlineKeyboardButton("📩 پشتیبانی تلگرام", url="https://t.me/…")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu_keyboard())

async def button_click(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "faq":
        # … مثل قبل …
        await q.edit_message_text("💥 سوالات …", reply_markup=main_menu_keyboard())
    elif q.data == "license":
        await q.edit_message_text("💳 شرایط …", reply_markup=main_menu_keyboard())
    elif q.data == "card":
        await q.edit_message_text("💳 شماره کارت …", reply_markup=main_menu_keyboard())

app_bot.add_handler(CommandHandler("start", start_cmd))
app_bot.add_handler(CallbackQueryHandler(button_click))
# ----------------------

# ----- وب‌سرور Flask برای دریافت وبهوک -----
server = Flask(__name__)

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot.bot)
    app_bot.update_queue.put(update)
    return "OK"

if __name__ == "__main__":
    # ست کردن وبهوک روی تلگرام
    app_bot.bot.set_webhook(f"{DOMAIN}/{BOT_TOKEN}")

    # راه‌اندازی Flask
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)

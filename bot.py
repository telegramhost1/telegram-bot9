from flask import Flask, request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
import os
import asyncio
import threading

BOT_TOKEN = os.environ["BOT_TOKEN"]
DOMAIN = os.environ["WEBHOOK_URL"]

app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

# ---------- دستور start ----------
async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("❓ سوالات پر تکرار", callback_data="faq")],
        [InlineKeyboardButton("📜 مجوزها", callback_data="license")],
        [InlineKeyboardButton("💳 شماره کارت", callback_data="card")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به ربات خوش آمدید. یک گزینه را انتخاب کنید 👇", reply_markup=reply_markup)

# ---------- پاسخ به دکمه‌ها ----------
async def button_click(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    
    if q.data == "faq":
        await q.edit_message_text("❓ سوالات پر تکرار:", reply_markup=main_menu_keyboard())
    elif q.data == "license":
        await q.edit_message_text("📜 مجوزها:", reply_markup=main_menu_keyboard())
    elif q.data == "card":
        await q.edit_message_text("💳 شماره کارت:", reply_markup=main_menu_keyboard())

# ---------- کیبورد اصلی ----------
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("❓ سوالات پر تکرار", callback_data="faq")],
        [InlineKeyboardButton("📜 مجوزها", callback_data="license")],
        [InlineKeyboardButton("💳 شماره کارت", callback_data="card")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- ثبت هندلرها ----------
app_bot.add_handler(CommandHandler("start", start_cmd))
app_bot.add_handler(CallbackQueryHandler(button_click))

# ---------- سرور Flask ----------
server = Flask(__name__)

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot.bot)
    app_bot.update_queue.put(update)
    return "OK"

# ---------- اجرای webhook در ترد جدا ----------
def set_webhook():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.bot.set_webhook(f"{DOMAIN}/{BOT_TOKEN}"))

if __name__ == "__main__":
    threading.Thread(target=set_webhook).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)

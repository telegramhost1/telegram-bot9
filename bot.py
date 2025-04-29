from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

# ---------- پاسخ‌ها ----------
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("❓ سوالات پر تکرار", callback_data="faq")],
        [InlineKeyboardButton("📜 مجوزها", callback_data="license")],
        [InlineKeyboardButton("💳 شماره کارت", callback_data="card")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به ربات خوش آمدید 👇", reply_markup=main_menu_keyboard())

async def button_click(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(f"✅ انتخاب شما: {q.data}", reply_markup=main_menu_keyboard())

# ---------- هندلرها ----------
app_bot.add_handler(CommandHandler("start", start_cmd))
app_bot.add_handler(CallbackQueryHandler(button_click))

# ---------- سرور ----------
server = Flask(__name__)

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot.bot)
    app_bot.update_queue.put(update)
    return "OK"

# ---------- Webhook setup ----------
def set_webhook():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.bot.set_webhook(f"{DOMAIN}/{BOT_TOKEN}"))

if __name__ == "__main__":
    threading.Thread(target=set_webhook).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)

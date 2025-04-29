import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
DOMAIN = os.environ["WEBHOOK_URL"]  # مثل: https://telegram-bot9-leuz.onrender.com

# ---------- کیبورد ---------- #
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("❓ سوالات پر تکرار", callback_data="faq")],
        [InlineKeyboardButton("📜 مجوزها", callback_data="license")],
        [InlineKeyboardButton("💳 شماره کارت", callback_data="card")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- فرمان /start ---------- #
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "به ربات خوش آمدید 👇",
        reply_markup=main_menu_keyboard()
    )

# ---------- پاسخ به دکمه‌ها ---------- #
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    responses = {
        "faq": "❓ سوالات پر تکرار:",
        "license": "📜 مجوزها:",
        "card": "💳 شماره کارت:"
    }
    await query.edit_message_text(
        text=responses.get(query.data, "خطا!"),
        reply_markup=main_menu_keyboard()
    )

# ---------- اجرای Webhook ---------- #
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CallbackQueryHandler(button_click))

    await app.bot.set_webhook(url=f"{DOMAIN}/{BOT_TOKEN}")

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=BOT_TOKEN,
        webhook_url=f"{DOMAIN}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن ربات
app = ApplicationBuilder().token("8000438969:AAFhj0ZEcVUehcY268sXcb26DUnCOiANlj8").build()

# آیدی پشتیبانی
support_id = "@Unlock_mobile_com"

# منوی دکمه‌های درون‌خطی
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
            "در مورد دوره بازیابی رمز گوشی\n\n"
            "🔹 چه مدل گوشی‌هایی رو میشه باز کرد؟\n"
            "سامسونگ، شیائومی، هوآوی با CPU مدیاتک، کوالکام، اگزینوس\n\n"
            "🔹 نیاز به باکس؟ خیر، فقط دو نرم‌افزار نیاز هست که بعد از خرید ارسال می‌شود\n\n"
            "🔹 ویندوز موردنیاز؟ ویندوز 10 پرو، 64 بیت\n"
            "🔹 سخت‌افزار؟ i5 به بالا، رم 8 گیگ، هارد SSD فرمت GPT\n\n"
            "🔹 آموزش ویدیویی؟ بله، در سایت موجود است\n"
            "🔹 پشتیبانی؟ تلگرام و واتساپ\n"
            "🔹 آپدیت؟ بله\n\n"
            "🔹 نرم‌افزار MD NEXT تا اندروید 8 بدون حذف اطلاعات\n"
            "🔹 نرم‌افزار OXYGEN تا نسخه‌های جدید اندروید\n\n"
            "📌 مدل‌های قابل پشتیبانی پس از وارد کردن مدل در نرم‌افزار نمایش داده می‌شوند\n\n"
            f"📩 پشتیبانی: {support_id}",
            reply_markup=main_menu_keyboard()
        )

    elif query.data == "license":
        await query.edit_message_text(
            "💳 شرایط خرید لایسنس:\n\n"
            "۱- ابتدا آموزش نصب را از سایت مشاهده کنید.\n"
            "۲- پس از پرداخت و ارسال رسید به پشتیبانی، فایل نصب و کرک ارسال می‌شود.\n"
            "۳- بعد از نصب، Hardware ID سیستم خود را به پشتیبانی بفرستید تا لایسنس برای شما ساخته شود.\n\n"
            f"📩 پشتیبانی: {support_id}",
            reply_markup=main_menu_keyboard()
        )

    elif query.data == "card":
        await query.edit_message_text(
            "💳 شماره کارت جهت واریز:\n\n"
            "🔹 شماره کارت: ‎6104-3373-6006-3620‎\n"
            "🔹 صاحب حساب: بهزاد خزانی\n\n"
            "بعد از پرداخت لطفاً این موارد را به پشتیبانی ارسال کنید:\n"
            "- نام نرم‌افزار خریداری شده\n"
            "- نام و نام خانوادگی\n"
            "- شماره موبایل\n"
            "- تصویر رسید واریز\n\n"
            f"📩 پشتیبانی: {support_id}",
            reply_markup=main_menu_keyboard()
        )

# ثبت فرمان‌ها
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

# اجرای ربات
app.run_polling()

# از یک ایمیج سبک پایتون شروع می‌کنیم
FROM python:3.11-slim

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه به داخل کانتینر
COPY . .

# نصب نیازمندی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# مشخص کردن پورت
ENV PORT=8080

# اجرای پروژه
CMD ["python", "bot.py"]

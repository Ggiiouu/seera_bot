import telegram
from telegram.ext import Updater, MessageHandler, Filters
import os
import requests

# تابع برای اتصال به API Hugging Face
def query_huggingface(prompt, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 50, "num_return_sequences": 1}
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/HuggingFaceTB/SmolLM3-3B",
        headers=headers,
        json=payload
    )
    if response.status_code == 200:
        return response.json()[0]["generated_text"].strip()
    else:
        return "خطا در اتصال به مدل. لطفاً دوباره امتحان کنید."

# تابع برای مدیریت پیام‌ها
def handle_message(update, context):
    user_message = update.message.text
    api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    # پاسخ اولیه منشی
    if user_message.lower() in ['سلام', 'hi']:
        update.message.reply_text("سلام! من منشی شما هستم. چه کمکی می‌تونم بهتون بکنم؟")
    else:
        # ارسال پیام به API و دریافت پاسخ
        try:
            response = query_huggingface(user_message, api_token)
            update.message.reply_text(response)
        except Exception as e:
            update.message.reply_text("مشکلی پیش اومد! دوباره امتحان کنید.")

# راه‌اندازی بات
TOKEN = os.getenv('7653167541:AAEpXt7931UbGrweH1VvE_zj1YsNdWMhu54')  # توکن تلگرام از متغیر محیطی
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# اضافه کردن هندلر برای پیام‌ها
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# شروع بات
updater.start_polling()
updater.idle()
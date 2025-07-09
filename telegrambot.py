import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from huggingface_hub import InferenceClient

# خواندن توکن‌ها از متغیرهای محیطی (برای دیپلوی)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_API_KEY = os.environ.get("HF_API_KEY")

client = InferenceClient(api_key=HF_API_KEY)

user_conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('سلام! به @Seera خوش اومدی! 😊 من منشی همه‌کاره‌تم، بگو چی تو سرته؟')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_message = update.message.text
    await update.message.reply_text('در حال فکر کردن... 🤔')

    if user_id not in user_conversations:
        user_conversations[user_id] = []

    prompt = f"تو یه منشی همه‌کاره به اسم @Seera هستی که برای مطب‌ها، شرکت‌ها و خدمات مختلف کار می‌کنی. وظایفت شامل رزرو نوبت، نمایش نوبت‌ها و مدیریت پرداخت‌هاست. کاربر به فارسی باهات حرف می‌زنه. بر اساس پیام کاربر، بفهم چی می‌خواد:\n- اگه درباره رزرو نوبت یا وقت گرفتن حرف زد، بگو که نوع کسب‌وکار، زمان (YYYY-MM-DD HH:MM) و توضیحات رو بفرسته.\n- اگه درباره دیدن نوبت‌ها پرسید، بگو که می‌تونی لیست نوبت‌هاش رو نشون بدی.\n- اگه درباره پرداخت یا هزینه پرسید، بگو که می‌تونه لینک پرداخت بگیره.\n- اگه فقط سلام کرد یا چیز نامشخصی گفت، یه جواب صمیمی و دعوت‌کننده بده.\nپیام کاربر: {user_message}"
    user_conversations[user_id].append({"role": "user", "content": prompt})

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            messages=user_conversations[user_id],
            max_tokens=500,
        )
        response_text = completion.choices[0].message["content"]
        user_conversations[user_id].append({"role": "assistant", "content": response_text})
        await update.message.reply_text(response_text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text('مشکلی پیش اومد! 😥')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("ربات در حال اجرا است...")
    app.run_polling()

if __name__ == '__main__':
    main()
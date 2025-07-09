import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from huggingface_hub import InferenceClient

# توکن‌ها از متغیر محیطی
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_API_KEY = os.environ.get("HF_API_KEY")
PORT = int(os.environ.get("PORT", 8443))  # پورت پیش‌فرض

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

    prompt = f"تو یه منشی همه‌کاره به اسم @Seera هستی... [بقیه پرامپتت]\nپیام کاربر: {user_message}"
    user_conversations[user_id].append({"role": "user", "content": prompt})

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            messages=user_conversations[user_id],
            max_tokens=150,
        )
        response_text = completion.choices[0].message["content"]
        user_conversations[user_id].append({"role": "assistant", "content": response_text})
        await update.message.reply_text(response_text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text('مشکلی پیش اومد! 😥')

async def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    # استفاده از webhook با پورت
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN
    )

if __name__ == "__main__":
    asyncio.run(run_bot())
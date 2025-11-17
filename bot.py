from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# -------------------------
# تنظیمات
# -------------------------
BOT_TOKEN = "8495622135:AAEdNbSZIMU4nOlAEKCtCEWmsGDmwshQarU"
WEBHOOK_URL = "https://mb100.onrender.com/telegram_webhook"  # وبهوک واقعی خودتان

# متغیر برای ذخیره آخرین شماره
last_number = "null"

# -------------------------
# ایجاد FastAPI و Bot
# -------------------------
app = FastAPI()
application = ApplicationBuilder().token(BOT_TOKEN).build()

# -------------------------
# هندلر پیام
# -------------------------
async def handle_message(update: Update, context):
    global last_number
    text = update.message.text.strip()

    if not text.isdigit() or len(text) != 4:
        await update.message.reply_text("⚠️ Please send a 4-digit number only.")
        return

    last_number = text
    await update.message.reply_text(f"✔️ Number {text} saved. ESP32 can fetch it now.")

# -------------------------
# وبهوک FastAPI
# -------------------------
@app.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# -------------------------
# API برای ESP32
# -------------------------
@app.get("/get_number")
def get_number():
    global last_number
    return {"number": last_number}

# -------------------------
# رویداد startup
# -------------------------
@app.on_event("startup")
async def on_startup():
    # ثبت هندلر
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    # ثبت وبهوک در تلگرام
    await application.bot.set_webhook(WEBHOOK_URL)

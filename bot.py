# bot.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ====== تنظیمات ======
BOT_TOKEN = "8495622135:AAEdNbSZIMU4nOlAEKCtCEWmsGDmwshQarU"
WEBHOOK_URL = "https://mb100.onrender.com/telegram_webhook"  # لینک برنامه شما روی Render
# ====================

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

# متغیر ذخیره عدد
last_number = "5000"

# ===== مسیر برای آردوینو =====
@app.get("/get_number")
async def get_number():
    return JSONResponse(content={"number": last_number})

# ===== مسیر webhook تلگرام =====
@app.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await handle_message(update, ContextTypes.DEFAULT_TYPE(application=None))
    return "ok"

# ===== مدیریت پیام های دریافتی =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_number
    text = update.message.text

    if text.isdigit() and len(text) == 4:
        last_number = text
        await update.message.reply_text(f"✔️ Number saved: {text}")
    else:
        await update.message.reply_text("❌ Please send a 4-digit number.")

# ===== برنامه تلگرام =====
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# ===== استارت FastAPI =====
@app.on_event("startup")
async def on_startup():
    # ست کردن webhook
    await bot.set_webhook(WEBHOOK_URL)



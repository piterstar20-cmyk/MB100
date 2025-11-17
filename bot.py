# bot.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8495622135:AAEdNbSZIMU4nOlAEKCtCEWmsGDmwshQarU"
WEBHOOK_URL = "https://mb100.onrender.com/telegram_webhook"

app = FastAPI()
last_number = "9800"

# مسیر آردوینو
@app.get("/get_number")
async def get_number():
    return JSONResponse(content={"number": last_number})

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_number
    text = update.message.text
    if text.isdigit() and len(text) == 4:
        last_number = text
        await update.message.reply_text(f"✔️ Number saved: {text}")
    else:
        await update.message.reply_text("❌ Please send a 4-digit number.")

# مسیر webhook تلگرام
@app.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "ok"

# ساخت Application تلگرام
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# هنگام استارت FastAPI، Webhook را ست می‌کنیم
@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(WEBHOOK_URL)

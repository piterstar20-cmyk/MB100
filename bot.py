from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import os
import asyncio

app = FastAPI()

# --- Stores the last number received from Telegram ---
last_number = "null"

# --- Load bot token and webhook URL from environment variables ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Set this in Render environment
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Example: https://yourapp.onrender.com/telegram_webhook

bot = Bot(token=BOT_TOKEN)

# --- API endpoint for ESP32 ---
@app.get("/get_number")
def get_number():
    global last_number
    return {"number": last_number}

# --- Telegram message handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_number

    text = update.message.text.strip()

    if not text.isdigit() or len(text) != 4:
        await update.message.reply_text("⚠️ Please send only a 4-digit number.")
        return

    last_number = text
    await update.message.reply_text(f"✔️ Number {text} saved. ESP32 can now fetch it.")

# --- FastAPI endpoint for Telegram Webhook ---
@app.post("/telegram_webhook")
async def telegram_webhook(req: Request):
    update = Update.de_json(await req.json(), bot)
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Process the update
    await handle_message(update, ContextTypes.DEFAULT_TYPE())
    return {"ok": True}

# --- Set Telegram Webhook on startup ---
@app.on_event("startup")
async def startup_event():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to: {WEBHOOK_URL}")

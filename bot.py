from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ContextTypes, MessageHandler, filters
import asyncio

app = FastAPI()

# --- Stores the last number received from Telegram ---
last_number = "null"

# --- Directly set your bot token and webhook URL here ---
BOT_TOKEN = "8495622135:AAEdNbSZIMU4noEWmsGDmwshQarU"
WEBHOOK_URL = "https://mb100.onrender.com/telegram_webhook"

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
    await handle_message(update, ContextTypes.DEFAULT_TYPE())
    return {"ok": True}

# --- Set Telegram Webhook on startup ---
@app.on_event("startup")
async def startup_event():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to: {WEBHOOK_URL}")


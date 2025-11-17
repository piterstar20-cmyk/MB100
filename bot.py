from fastapi import FastAPI
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import asyncio

app = FastAPI()

# --- Stores the last number received from Telegram ---
last_number = "null"

BOT_TOKEN = "8208471979:AAHXGkqSG1B2tfH_kwVv_evwKNxjhItV_K4"


# --- API endpoint for ESP32 ---
@app.get("/get_number")
def get_number():
    global last_number
    return {"number": last_number}


# --- Telegram message handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_number

    text = update.message.text.strip()

    # Check if message is a 4-digit number
    if not text.isdigit() or len(text) != 4:
        await update.message.reply_text("⚠️ Please send a 4-digit number only.")
        return

    last_number = text
    await update.message.reply_text(f"✔️ Number {text} saved. ESP32 can fetch it now.")


# --- Start Telegram bot in background ---
async def start_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # در نسخه 20+ همین کافی است:
    await app_bot.run_polling()



# --- FastAPI startup event ---
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())



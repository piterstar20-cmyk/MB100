# bot.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Update, Bot

# ====== تنظیمات ======
BOT_TOKEN = "8495622135:AAEdNbSZIMU4nOlAEKCtCEWmsGDmwshQarU"
WEBHOOK_URL = "https://mb100.onrender.com/telegram_webhook"
# ====================

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

# ذخیره عدد آخر + پرچم جدید بودن داده
last_number = ""
new_data_available = False


# ===== مسیر برای آردوینو =====
@app.get("/get_number")
async def get_number():
    global new_data_available, last_number

    if new_data_available:
        # عدد را یکبار ارسال می‌کنیم
        response = {"new": True, "number": last_number}
        new_data_available = False   # فلگ صفر می‌شود
        return JSONResponse(content=response)

    # داده‌ای نیست
    return JSONResponse(content={"new": False})
    

# ===== مسیر webhook تلگرام =====
@app.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    global last_number, new_data_available

    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.text:

        text = update.message.text.strip()

        if text.isdigit() and len(text) == 4:
            last_number = text
            new_data_available = True  # فقط همینجا True می‌شود
            await bot.send_message(update.message.chat_id, f"✔️ Number saved: {text}")
        else:
            await bot.send_message(update.message.chat_id, "❌ Please send a 4-digit number.")

    return "ok"


# ===== ست کردن webhook =====
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from database import db

TOKEN = "ВАШ_ТОКЕН_БОТА"  # Укажите токен бота
PRIVATE_CHANNEL = "@ВАШ_КАНАЛ"  # Укажите ссылку на ваш закрытый канал

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Кнопка оплаты
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)", 
                   (message.from_user.id, message.from_user.username))
    db.commit()

    pay_button = InlineKeyboardMarkup(row_width=1)
    pay_button.add(InlineKeyboardButton("Оплатить", callback_data="pay"))
    await message.reply("Добро пожаловать! Оплатите подписку для доступа к каналу.", reply_markup=pay_button)

# Генерация ссылки на оплату
@dp.callback_query_handler(lambda c: c.data == "pay")
async def process_payment(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    payment_link = f"https://your-payment-page.example.com?user_id={user_id}"
    await bot.send_message(user_id, f"Оплатите по ссылке: {payment_link}")

# Удаление из канала
async def check_subscriptions():
    cursor = db.cursor()
    users = cursor.execute("SELECT telegram_id, subscription_end FROM users WHERE payment_status = TRUE").fetchall()
    for telegram_id, subscription_end in users:
        if datetime.strptime(subscription_end, "%Y-%m-%d %H:%M:%S") < datetime.now():
            await bot.kick_chat_member(chat_id=PRIVATE_CHANNEL, user_id=telegram_id)
            cursor.execute("UPDATE users SET payment_status = FALSE WHERE telegram_id = ?", (telegram_id,))
            db.commit()

scheduler = AsyncIOScheduler()
scheduler.add_job(check_subscriptions, "interval", hours=1)
scheduler.start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

from multiprocessing import Process
from aiogram import Bot, Dispatcher, executor
from flask import Flask, request
import asyncio

# Инициализация бота
API_TOKEN = 7916564478:AAG8rJNZTwuavj06h_xy-yBi7rvKY0q-FzA
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await message.reply("Привет! Я ваш бот.")

# Функция для запуска бота
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True)

# Инициализация Flask-приложения
app = Flask(__name__)

@app.route('/')
def index():
    return "Сервер работает!"

# Функция для запуска веб-сервера
def start_web():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    p1 = Process(target=start_bot)
    p2 = Process(target=start_web)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

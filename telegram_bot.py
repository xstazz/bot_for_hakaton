import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from Token import TOKEN
API_TOKEN = TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Подключение к базе данных SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
username, password = '', ''
print('SELECT * FROM users WHERE username=? AND password=?')
# Функция для проверки входа пользователя
async def check_login(username: str, password: str) -> bool:
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    return True if user else False

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Для входа используй команду /login")

# Обработка команды /login
@dp.message_handler(commands=['login'])
async def cmd_login(message: types.Message):
    await message.reply("Введите ваш логин и пароль через пробел, например: login пароль")

# Обработка сообщений пользователя
@dp.message_handler()
async def echo(message: types.Message):
    user_input = message.text.split()
    if len(user_input) != 2:
        await message.reply('Неверный формат! Используйте: login пароль')
        return

    username, password = user_input
    if await check_login(username, password):
        await message.reply('Вход выполнен успешно!')
    else:
        await message.reply('Неверный логин или пароль!')

# Обработка неизвестных команд
@dp.message_handler(lambda message: message.text.startswith('/'))
async def unknown(message: types.Message):
    await message.reply("Извините, я не понимаю эту команду.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

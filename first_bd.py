import asyncio
import logging
import sqlite3 as sl
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import TOKEN
import os

# открываем файл с базой данных
# users = sl.connect('users.db')

logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

# cursor = users.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#             	(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет")
    users = sl.connect('users.db')
    id_user = message.from_user.id
    cursor = users.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                	(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    users.commit()
    cursor.execute(f'INSERT INTO users (id, name, age) VALUES ({id_user}, "Саня", 18)')
    users.commit()
    cursor.close()
    users.close()
    s = str(message.from_user.id)
    await message.answer(s)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())

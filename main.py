import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import core.handlers.start
from core.config import TOKEN

from core.handlers import registration, start, change_user_data, main_menu, delete_acc, second_check, first_check, diagnostic


logging.basicConfig(level=logging.INFO)


async def main():

    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                	(id INTEGER PRIMARY KEY, name TEXT, age INTEGER, sex TEXT, hypertension INTEGER, heart_disease INTEGER, ever_married INTEGER, urban_dweller INTEGER, avg_glucose_level 
    INTEGER, bmi INTEGER, smoking_status INTEGER, cp INTEGER, trtbps INTEGER, chol INTEGER, fbs INTEGER, restecg INTEGER, thalach INTEGER, exng INTEGER, slope INTEGER, ca INTEGER, brain_photo TEXT, brain_result INTEGER, test1_result INTEGER)''')
    users.commit()

    
    bot=Bot(token=TOKEN)
    dp = Dispatcher()  
    dp.include_routers(start.router, registration.router, change_user_data.router, main_menu.router, delete_acc.router, diagnostic.router, second_check.router, first_check.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ =="__main__":
    asyncio.run(main())
import asyncio
from aiogram import Bot, Dispatcher, F, Router
import logging
import sqlite3 as sl
from core.config import config
from core.handlers import brain_test, registration, start, change_user_data, main_menu, delete_acc, second_check, first_check, xray_test


logging.basicConfig(level=logging.INFO)


async def main():
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                	(id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    sex TEXT,
                    hypertension INTEGER,
                    heart_disease INTEGER,
                    ever_married INTEGER,
                    urban_dweller INTEGER,
                    avg_glucose_level INTEGER,
                    bmi INTEGER,
                    smoking_status INTEGER,
                    cp INTEGER, trtbps INTEGER,
                    chol INTEGER,
                    fbs INTEGER,
                    restecg INTEGER,
                    thalach INTEGER,
                    exng INTEGER,
                    slope INTEGER,
                    ca INTEGER,
                    brain_image TEXT,
                    brain_result INTEGER,
                    xray_image TEXT,
                    xray_result INTEGER,
                    first_check_result INTEGER,
                    second_check_result INTEGER
                    )''')
    users.commit()

    
    bot=Bot(config.token)
    dp = Dispatcher()  
    dp.include_routers(start.router,
                    registration.router,
                    change_user_data.router,
                    main_menu.router,
                    delete_acc.router,
                    brain_test.router,
                    second_check.router,
                    first_check.router, 
                    xray_test.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ =="__main__":
    asyncio.run(main())
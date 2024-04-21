import asyncio
from aiogram import Bot, Dispatcher, F, Router
import logging
import sqlite3 as sl
from core.config import config
from core.handlers import brain_test, registration, start, change_user_data, main_menu, delete_acc, second_check, first_check, xray_test, show_hospitals


logging.basicConfig(level=logging.INFO)


async def main():
    users = sl.connect('core/users.db')
    users_cursor = users.cursor()
    users_cursor.execute('''CREATE TABLE IF NOT EXISTS users
                	(key INTEGER,
                    additional_key TEXT,
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
                    second_check_result INTEGER,
                    PRIMARY KEY(key, additional_key)
                    )''')
    users.commit()

    hospitals = sl.connect('core/hospitals.db')
    hospitals_cursor = hospitals.cursor()
    hospitals_cursor.execute('''
                                CREATE TABLE IF NOT EXISTS hospitals
                             (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT,
                             disease TEXT,
                             coord_x INTEGER,
                             coord_y INTEGER
                             )
                            ''')
    hospitals.commit()
    # hospitals = sl.connect('core/hospitals.db')
    hospitals_cursor = hospitals.cursor()
    data = [
        ("Лахта клиника", "pneumonia", 59.937250, 30.356190),
        ("XII век", "pneumonia", 59.924017, 30.351108)
    ]
    hospitals_cursor.executemany('INSERT INTO hospitals (name, disease, coord_x, coord_y) VALUES (?, ?, ?, ?)', data)
    hospitals.commit()
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
                    xray_test.router,
                    show_hospitals.router
                    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ =="__main__":
    asyncio.run(main())
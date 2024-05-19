import asyncio
from aiogram import Bot, Dispatcher, F, Router
import logging
import sqlite3 as sl
from core.config import config
from core.handlers import start, brain_test, registration,  change_user_data, main_menu, delete_acc, second_check, first_check, xray_test, show_hospitals, dialogue_with_doctor, show_test_results
# from core.tests.test_handlers import test_start

logging.basicConfig(level=logging.INFO)


bot=Bot(config.token)


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
    users_cursor.close()
    users.close()

    doctors = sl.connect('core/doctors.db')
    doctors_cursor = doctors.cursor()
    doctors_cursor.execute('''
                    CREATE TABLE IF NOT EXISTS doctors
                    (
                    key INTEGER PRIMARY KEY,
                    username TEXT,
                    firstname TEXT,
                    surname TEXT,
                    city TEXT,
                    work_address TEXT,
                    name_organization TEXT,
                    disease TEXT
                    )
            ''')
    doctors.commit()
    doctors_cursor.close()
    doctors.close()
   
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
                    show_hospitals.router,
                    dialogue_with_doctor.router,
                    show_test_results.router
                    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ =="__main__":
    asyncio.run(main())
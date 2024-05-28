import asyncio
from aiogram import Bot, Dispatcher, F, Router
import logging
import sqlite3 as sl
from core.config import config
from core.handlers import start, brain_test, registration,  change_user_data, main_menu, delete_acc, second_check, first_check, xray_test, show_hospitals, dialogue_with_doctor, show_test_results, full_checkup
from core.sql_utils import create_users_table, connect_to_postgres, drop_table, create_doctors_table, insert_doctor, drop_doctors_table, get_doctor_by_disease

logging.basicConfig(level=logging.INFO)


bot=Bot(config.token)


async def main():
    conn = await connect_to_postgres()
    # await drop_table(conn)
    await create_users_table(conn)
    # await drop_doctors_table(conn)
    # await create_doctors_table(conn)
    # data = [
    # ('@natlad', 'Наталья', 'Ладошкина', 'Saint Petersburg', 'Большой Сампсониевский проспект, 45','XXI век', 'pneumonia'),
    # ('@Lafillek', 'Ксения', 'Быкова', 'Saint Petersburg', 'Ковенский переулок, 5', 'Лахта клиника', 'pneumonia'),
    # ('@kpvap', 'Кирилл', 'Алметов', 'Saint Petersgurg', 'Большой проспект Васильевского острова, 49-51', 'Клиника Пирогова', 'diabetes'),
    # ('@era1ash', 'Степан', 'Демьянов', 'Saint Petersburg', 'Финский переулок, 4','Клиника Источник', 'diabetes'),
    # ]
    # await insert_doctor(data)   
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
                    show_test_results.router,
                    full_checkup.router
                    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ =="__main__":
    asyncio.run(main())
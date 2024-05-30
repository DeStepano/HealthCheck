import asyncio
from aiogram import Bot, Dispatcher
import logging
import sqlite3 as sl
from core.config import config
from core.handlers import diabetes, start, brain_test, registration,  change_user_data, main_menu, delete_acc, xray_test, show_hospitals, dialogue_with_doctor, show_test_results, full_checkup
from core.sql_utils import create_users_table, connect_to_postgres

logging.basicConfig(level=logging.INFO)


bot=Bot(config.token)


async def main():
    conn = await connect_to_postgres()
    await create_users_table(conn)
    dp = Dispatcher()  
    dp.include_routers(start.router,
                    registration.router,
                    change_user_data.router,
                    main_menu.router,
                    delete_acc.router,
                    brain_test.router,
                    diabetes.router, 
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
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from core.handlers.basic import start
from core.settings import settings


async def main():
    bot = Bot(token=settings.bots.bot_token)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher()
    dp.message.register(start)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    
    asyncio.run(main())
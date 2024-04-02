import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import logging
from core.hash import get_hash
from core.keyboards import keyboards
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    keys = await get_hash(message.from_user.id)
    users = sl.connect('core/users.db')
    cur = users.cursor()
    cur.execute("""SELECT COUNT(*) FROM users WHERE key = ? AND additional_key = ?""", (keys[0], keys[1]))
    row_count = cur.fetchone()[0]
    cur.close()
    users.close()

    if(row_count > 0):
        users = sl.connect('core/users.db')
        cur = users.cursor()
        cur.execute("""SELECT name FROM users WHERE key = ? AND additional_key = ?""", (keys[0], keys[1]))
        row = cur.fetchone()
        cur.close()
        users.close()
        await message.answer(F"Привет, {row[0]}!", reply_markup=keyboards.main_kb)

    else:
        await message.answer("Привет, я бот, позволяющий выявлять наличие заболеваний, основываясь на результатах опросов и изображений медецинских анализов. Чтобы пользоваться мной, необходимо зарегистрироваться!",
                             reply_markup=keyboards.registration_kb)


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer("Привет, я бот, который... Напиши /start, чтобы начать")

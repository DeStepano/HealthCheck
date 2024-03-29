import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import logging
from core.logic import get_hash
from core.keyboards import keyboards
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    id_user = await get_hash(message.from_user.id)
    users = sl.connect('core/users.db')
    cur = users.cursor()
    exists = cur.execute("SELECT 1 FROM users use WHERE id = ?", [id_user]).fetchone()
    cur.close()
    users.close()

    if (not exists):
        await message.answer("Привет, я бот, который... Чтобы пользоваться мной, необходимо зарегистрироваться!",
                             reply_markup=keyboards.registration_kb)
    else:
        # id_user = message.from_user.id
        users = sl.connect('core/users.db')
        cur = users.cursor()
        # exists = cur.execute("FROM users use WHERE id = ?", [id_user]).fetchone()
        exits = cur.execute("SELECT name FROM users WHERE id=?", [id_user]).fetchone()
        cur.close()
        users.close()
        await message.answer(F"Привет, {exits[0]}!", reply_markup=keyboards.main_kb)


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer("Привет, я бот, который... Напиши /start, чтобы начать")

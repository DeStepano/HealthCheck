from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards

router = Router()




@router.message(Command("Удалить_аккаунт"))
async def change_user_data(message: Message, state: FSMContext):
    await message.answer("Вы уверены?", reply_markup=keyboards.delete_kb)


@router.message(Command("Точно_удалить"))
async def change_user_data(message: Message, state: FSMContext):
    id_user = message.from_user.id
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id_user,))
    cursor.execute("UPDATE users SET id = id - 1 WHERE id > ?", (id_user,))
    users.commit()
    await message.answer("Успешно", reply_markup=keyboards.registration_kb)

@router.message(Command("Не_удалять"))
async def change_user_data(message: Message, state: FSMContext):
    await message.answer("Хорошо", reply_markup=keyboards.setting_kb)

from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards
from core.hash import get_hash


router = Router()

@router.message(Command("Удалить_аккаунт"))
async def change_user_data(message: Message, state: FSMContext):
    await message.answer("Вы уверены?", reply_markup=keyboards.delete_kb)


@router.message(Command("Точно_удалить"))
async def change_user_data(message: Message, state: FSMContext):
    keys = await get_hash(message.from_user.id)
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    brain_image = cursor.execute("""SELECT brain_image FROM users WHERE key = ? AND additional_key = ?""", keys).fetchone()[0]
    if brain_image != None:
        os.remove(f"{brain_image}")
    xray_image = cursor.execute("""SELECT xray_image FROM users WHERE key = ? AND additional_key = ?""", keys).fetchone()[0]
    if xray_image != None:
        os.remove(f"{xray_image}")
    cursor.execute("DELETE FROM users WHERE key = ? AND additional_key = ?", keys)
    users.commit()
    cursor.close()
    users.close()
    await message.answer("Успешно", reply_markup=keyboards.registration_kb)


@router.message(Command("Не_удалять"))
async def change_user_data(message: Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=keyboards.setting_kb)

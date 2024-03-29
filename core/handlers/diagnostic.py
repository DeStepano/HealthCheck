from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import hashlib
import logging
import sqlite3 as sl
import uuid
import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.logic import get_hash
router = Router()

dp = Dispatcher()

class Form(StatesGroup):
    photo = State()

global bot

@router.message(Command("Болезнь_1"), StateFilter(None))
async def settings(message: Message, state: FSMContext):
    await state.set_state(Form.photo)
    await message.answer("Прикрепите фото", reply_markup=keyboards.diagnostic_kb)


@router.message(F.photo, Form.photo)
async def photo_message(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo = message.photo[-1])
    user_id = await get_hash(message.from_user.id)
    data = await state.get_data()
    await state.clear()
    path = f"/home/sasha/health_checker/HealthCheck/images/{data['photo'].file_id + str(uuid.uuid4())}.jpg"
    await bot.download(
        data['photo'],
        destination=path
    )
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute('UPDATE users SET brain_photo = ? WHERE id = ?', (path, user_id))
    users.commit()
    cursor.close()
    users.close()
    await message.answer("Фото получено")


@router.message(Form.photo)
async def incorrect_photo(message: Message):
    await message.answer("Это не фото, отправте фото")
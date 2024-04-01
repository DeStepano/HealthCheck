from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import uuid
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.hash import get_hash
from core.rcp_client import RcpClient
import base64
import json
from PIL import Image
from core.config import config


router = Router()

dp = Dispatcher()

class Form(StatesGroup):
    photo = State()

global bot

@router.message(Command("Болезнь_4"), StateFilter(None))
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
    cursor.execute('UPDATE users SET xray_image = ? WHERE id = ?', (path, user_id))
    users.commit()
    file_path = await bot.get_file(data['photo'].file_id)
    photo_binary_data = await bot.download_file(file_path.file_path)
    photo_binary_data = photo_binary_data.read()
    encoded_data = base64.b64encode(photo_binary_data)
    await message.answer("Фото получено. Начат анализ...")
    result = json.loads(RcpClient.call(encoded_data, config.xray_queue))
    cursor.execute('UPDATE users SET xray_result = ? WHERE id = ?', (result, user_id))
    await message.answer(f"Ваш результат: {result}")
    users.commit()
    cursor.close()
    users.close()


@router.message(Form.photo)
async def incorrect_photo(message: Message):
    await message.answer("Это не фото, отправте фото")
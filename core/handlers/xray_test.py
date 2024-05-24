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
from core.rcp_client import rpcClient
import base64
import json
import cv2
from core.config import config
from core.states import States
import numpy as np

router = Router()
dp = Dispatcher()

class Form(StatesGroup):
    photo_xray = State()

global bot

@router.message(Command("Флюорография"), StateFilter(States.check_diseases_command))
async def settings(message: Message, state: FSMContext):
    await state.set_state(Form.photo_xray)
    await message.answer("Пришлите фото. Его размер должен быть не менее 128*128 пикселей", reply_markup=keyboards.diagnostic_kb)


@router.message(F.photo, Form.photo_xray)
async def photo_message(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo = message.photo[-1])
    key, additional_key = await get_hash(message.from_user.id)
    data = await state.get_data()
    file_path = await bot.get_file(data['photo'].file_id)
    photo_binary_data = await bot.download_file(file_path.file_path)
    image = cv2.imdecode(np.frombuffer(photo_binary_data.getvalue(), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    height = 0
    width = 0

    if image is not None:
        height, width = image.shape[:2]

    if width < 128 or height < 128:
        await message.answer("Размер фото слишком мал, пришлите другое")
    else:
        await state.set_state(States.check_diseases_command)
        await message.answer("Изображение получено, начат анализ")
        path = f"/home/sasha/health_checker/HealthCheck/images/{data['photo'].file_id + str(uuid.uuid4())}.jpg"
        await bot.download(
            data['photo'],
            destination=path
        )
        binary_data = photo_binary_data.read()
        encoded_data = base64.b64encode(binary_data)
        result = json.loads(rpcClient.call(encoded_data, config.xray_queue))
        await message.answer(f"Ваш результат: {result}")

@router.message(Form.photo_xray)
async def incorrect_photo(message: Message):
    await message.answer("Это не фото, отправте фото")
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import uuid
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.sql_utils import insert_data
from core.rpc_client import rpcClient
import base64
import json
from core.config import config
from core.states import States
from PIL import Image
from core.hash import get_hash_string


router = Router()
dp = Dispatcher()
global bot

class Form(StatesGroup):
    photo_brain = State()


@router.message(Command("Заболевания_мозга"), StateFilter(States.check_diseases_command))
async def settings(message: Message, state: FSMContext):
    await state.set_state(Form.photo_brain)
    await message.answer("Прикрепите фото вашего МРТ размера не меньше 150*150", reply_markup=keyboards.diagnostic_kb)


@router.message(F.photo, Form.photo_brain)
async def photo_message(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo = message.photo[-1])
    data = await state.get_data()
    file_path = await bot.get_file(data['photo'].file_id)
    photo_binary_data = await bot.download_file(file_path.file_path)
    image = Image.open(photo_binary_data)
    width, height = image.size
    if width < 150 or height < 150:
        await message.answer("Размер фото слишком мал, пришлите другое")
    else:
        await state.set_state(States.check_diseases_command)
        await message.answer("Изображение получено, начат анализ")
        file_name = await get_hash_string(data['photo'].file_id)
        path = f"/home/sasha/health_checker/HealthCheck/images/{file_name + str(uuid.uuid4())}.jpg"
        await bot.download(
            data['photo'],
            destination=path
        )
        user_id = message.from_user.id
        await insert_data("UPDATE users SET brain_image = $3 WHERE key = $1 AND additional_key = $2", (path,), user_id)
        photo_binary_data = await bot.download_file(file_path.file_path)
        photo_binary_data = photo_binary_data.read()
        encoded_data = base64.b64encode(photo_binary_data)
        result = json.loads(rpcClient.call(encoded_data, config.brain_analysis_queue))
        await insert_data('UPDATE users SET brain_result = $3 WHERE key = $1 AND additional_key = $2', (result,), user_id)
        await message.answer(f"Ваш результат: {result}")


@router.message(Form.photo_brain)
async def incorrect_photo(message: Message):
    await message.answer("Это не фото, отправте фото")
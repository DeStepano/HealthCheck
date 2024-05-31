from core.sql_utils import get_data_by_id, check_user
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import logging
from core.keyboards import keyboards
logging.basicConfig(level=logging.INFO)


router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user = await check_user(user_id)
    if(user > 0):
        name = await get_data_by_id("SELECT name FROM users WHERE key = $1 AND additional_key = $2", user_id)
        await message.answer(F"Привет, {name[0]}!", reply_markup=keyboards.main_kb)

    else:
        await message.answer("Привет, я бот, позволяющий выявлять наличие заболеваний, основываясь на результатах опросов и изображений медецинских анализов. Чтобы пользоваться мной, необходимо зарегистрироваться!",
                             reply_markup=keyboards.registration_kb)


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer("Привет, я бот, который... Напиши /start, чтобы начать")

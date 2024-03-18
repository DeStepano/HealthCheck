from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards

router = Router()

dp = Dispatcher()

class Form(StatesGroup):
    photo = State()

global bot

# @router.message(Command("Проверить_анализы"))
# async def settings(message: Message, state: FSMContext):
#     await message.answer("Выберете нужное", reply_markup=keyboards.diagnostic_kb)


@router.message(Command("Болезнь_1"), StateFilter(None))
async def settings(message: Message, state: FSMContext):
    await state.set_state(Form.photo)
    await message.answer("Прикрепите фото", reply_markup=keyboards.diagnostic_kb)


@router.message(F.photo, Form.photo)
async def photo_message(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo = message.photo[-1])
    data = await state.get_data()
    await state.clear()
    await bot.download(
        data['photo'],
        destination=f"\sasha\health_checker\HealthCheck\{data['photo'].file_id}.jpg"
    )
    await message.answer("Фото получено")


@router.message(Form.photo)
async def incorrect_photo(message: Message):
    await message.answer("Это не фото, отправте фото")
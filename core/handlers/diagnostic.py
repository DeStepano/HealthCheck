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

dp = Dispatcher()

class Form(StatesGroup):
    photo = State()


@router.message(F.text.lower() == "проверить анализы")
async def settings(message: Message, state: FSMContext):
    await message.answer("Выберете нужное", reply_markup=keyboards.diagnostic_kb)


@router.message(F.text.lower() == "болезнь 1")
async def settings(message: Message, state: FSMContext):
    await state.set_state(Form.photo)
    await message.answer("Прикрепите фото", reply_markup=keyboards.diagnostic_kb)


@router.message(F.photo)
async def photo_message(message: Message, state: FSMContext):
    photo_date = message.photo[-1]

    await message.answer(f'{photo_date}')

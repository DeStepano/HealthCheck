from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.states import States

router = Router()

@router.message(Command("Главное_меню"))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Главное меню",
        reply_markup=keyboards.main_kb
    )


@router.message(Command("Настройки"))
async def settings(message: Message):
    await message.answer("настройки", reply_markup=keyboards.setting_kb)


@router.message(Command("Проверить_анализы"))
async def settings(message: Message, state: FSMContext):
    await state.set_state(States.command_1)
    await message.answer("Выберете заболевание", reply_markup=keyboards.diagnostic_kb)


@router.message(Command("Больницы_рядом"))
async def settings(message: Message, state: FSMContext):
    await state.set_state(States.command_2)
    await message.answer("Выберете заболевание", reply_markup=keyboards.diagnostic_kb)
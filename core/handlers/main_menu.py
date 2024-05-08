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
async def check_analysis(message: Message, state: FSMContext):
    await state.set_state(States.check_diseases_command)
    await message.answer("Выберете заболевание", reply_markup=keyboards.diagnostic_kb)


@router.message(Command("Больницы_рядом"))
async def hospitals(message: Message, state: FSMContext):
    await state.set_state(States.show_hospitals_command)
    await message.answer("Выберете заболевание", reply_markup=keyboards.disease_kb)

@router.message(Command("Диалог_с_врачем"))
async def dialogue_doctor(message: Message, state: FSMContext):
    await state.set_state(States.dialogue_with_doctor)
    await message.answer("Выберете заболевание", reply_markup=keyboards.disease_kb)
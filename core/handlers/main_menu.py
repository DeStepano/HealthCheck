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

@router.message(Command("Главное_меню"))
async def insert_main_kb(message: Message):
    await message.answer("Главное меню", reply_markup=keyboards.main_kb)


@router.message(Command("Настройки"))
async def settings(message: Message):
    await message.answer("настройки", reply_markup=keyboards.setting_kb)


@router.message(Command("Проверить_анализы"))
async def settings(message: Message):
    await message.answer("Выберете нужное", reply_markup=keyboards.diagnostic_kb)


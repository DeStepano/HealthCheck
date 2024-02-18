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

@router.message(F.text.lower()=="настройки")
async def settings(message: Message):
    await message.answer("найтройки", reply_markup=keyboards.setting_kb)


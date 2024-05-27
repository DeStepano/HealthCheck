from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import logging
import sqlite3 as sl
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from aiogram.types import ReplyKeyboardRemove
from core.hash import get_hash
from aiogram import F
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from core.config import config
from core.rcp_client import rpcClient
from core.states import States
from aiogram.types import(
    CallbackQuery
)


class Form():
    first_ans = State()


router = Router()


@router.message(Command("Болезнь5"), StateFilter(States.check_diseases_command))
async def change_user_data(message: Message, state: FSMContext):
    await state.set_state(Form.first_ans)
    await message.answer("Выберете типы заболевания:")


# @router.message(Form.first_ans)


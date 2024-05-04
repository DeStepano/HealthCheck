from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
import json
from core.rcp_client import RpcClient
from core.config import config
from core.states import States
from aiogram.types import WebAppInfo
from core.keyboards import keyboards
# import requests

router = Router()

@router.message(Command("Болезнь_4"), StateFilter(States.show_hospitals_command))
async def get_sex(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Болезнь 4", reply_markup=keyboards.web_kb)



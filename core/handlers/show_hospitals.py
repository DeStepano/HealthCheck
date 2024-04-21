from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
import json
from core.rcp_client import RpcClient
from core.config import config
from core.hash import get_hash
from core.states import States



router = Router()

@router.message(Command("Болезнь_4"), StateFilter(States.command_2))
async def get_sex(message: Message, state: FSMContext):
    await message.answer("работает")
    await state.clear()

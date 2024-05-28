from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3 as sl
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
import json
from core.rcp_client import RpcClient
from core.config import config
from core.states import States
from core.keyboards import keyboards
import random
from core.sql_utils import get_doctor_by_disease
from main import bot

router = Router()

# data = [
#     ('@natlad', 'Наталья', 'Ладошкина', 'Saint Petersburg', 'Большой Сампсониевский проспект, 45','XXI век', 'pneumonia'),
#     ('@Lafillek', 'Ксения', 'Быкова', 'Saint Petersburg', 'Ковенский переулок, 5', 'Лахта клиника', 'pneumonia'),
#     ('@kpvap', 'Кирилл', 'Алметов', 'Saint Petersgurg', 'Большой проспект Васильевского острова, 49-51', 'Клиника Пирогова', 'diabetes'),
#     ('@era1ash', 'Степан', 'Демьянов', 'Saint Petersburg', 'Финский переулок, 4','Клиника Источник', 'diabetes'),
# ]


@router.message(Command("Пневмония"), StateFilter(States.dialogue_with_doctor))
async def pneumonia(message: Message, state: FSMContext):
    doctor_data = await get_doctor_by_disease("pneumonia")
    username, name, surename = doctor_data['username'], doctor_data['firstname'], doctor_data['surename']
    await message.answer(f'Перейдите в диалог: {username}, {name} {surename}')


@router.message(Command("Диабет"), StateFilter(States.dialogue_with_doctor))
async def diabetes(message: Message, state: FSMContext):
    doctor_data = await get_doctor_by_disease("diabetes")
    username, name, surename = doctor_data['username'], doctor_data['firstname'], doctor_data['surename']
    await message.answer(f'Перейдите в диалог: {username}, {name} {surename}')
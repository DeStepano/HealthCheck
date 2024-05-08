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

from main import bot

router = Router()

# data = [
#     ('@natlad', 'Наталья', 'Ладошкина', 'Saint Petersburg', 'Большой Сампсониевский проспект, 45','XXI век', 'pneumonia'),
#     ('@Lafillek', 'Ксения', 'Быкова', 'Saint Petersburg', 'Ковенский переулок, 5', 'Лахта клиника', 'pneumonia'),
#     ('@kpvap', 'Кирилл', 'Алметов', 'Saint Petersgurg', 'Большой проспект Васильевского острова, 49-51', 'Клиника Пирогова', 'diabetes'),
#     ('@era1ash', 'Степан', 'Демьянов', 'Saint Petersburg', 'Финский переулок, 4','Клиника Источник', 'diabetes'),
# ]


# doctors = sl.connect('core/doctors.db')
# doctors_cursor = doctors.cursor()


# doctors_cursor.executemany("INSERT INTO doctors (username, firstname, surname, city, work_address, name_organization, disease) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
# doctors.commit()

async def get_doctor_id(disease: str):
    doctors = sl.connect('core/doctors.db')
    doctors_cursore = doctors.cursor()
    doctors_cursore.execute(f"SELECT * FROM doctors WHERE disease = '{disease}' ")
    result = doctors_cursore.fetchall()
    number = random.randint(0, len(result) - 1)
    doctors_cursore.close()
    doctors.close()
    result = result[number]
    return (result[1], result[2], result[3])


@router.message(Command("Пневмония"), StateFilter(States.dialogue_with_doctor))
async def pneumonia(message: Message, state: FSMContext):
    # await state.clear()
    doctor_data = await get_doctor_id("pneumonia")
    username, name, surename = doctor_data
    await message.answer(f'Перейдите в диалог: {username}, {name} {surename}')


@router.message(Command("Диабет"), StateFilter(States.dialogue_with_doctor))
async def diabetes(message: Message, state: FSMContext):
    # await state.clear()
    doctor_data = await get_doctor_id("diabetes")
    username, name, surename = doctor_data
    await message.answer(f'Перейдите в диалог: {username}, {name} {surename}')
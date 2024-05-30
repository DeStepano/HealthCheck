from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.config import config
from core.states import States
from core.sql_utils import get_doctor_by_disease
from main import bot


router = Router()


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
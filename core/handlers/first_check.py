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

class Form2(StatesGroup):
    hypertension = State()
    heart_disease = State()
    ever_married = State()
    urban_dweller = State()
    avg_glucose_level = State()
    bmi = State()
    smoking_status = State()


router = Router()


@router.message(Command("Болезнь_3"), StateFilter(States.command_1))
async def get_sex(message: Message, state: FSMContext):
    await state.set_state(Form2.hypertension)
    await message.answer("Есть ли у Вас гипертония?", reply_markup=keyboards.survey_kb)


@router.message(Form2.hypertension, F.text.casefold().in_(["да", "нет"]))
async def get_age(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "да":
        await state.update_data(hypertension=1)
    else:
        await state.update_data(hypertension=0)
    await state.set_state(Form2.heart_disease)
    await message.answer("Есть ли у Вас сердечные заболевания?", reply_markup=keyboards.survey_kb)


@router.message(Form2.heart_disease, F.text.casefold().in_(["да", "нет"]))
async def get_age(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "да":
        await state.update_data(heart_disease=1)
    else:
        await state.update_data(heart_disease=0)
    await state.set_state(Form2.ever_married)
    await message.answer("Состояли/состоите ли Вы в браке?", reply_markup=keyboards.survey_kb)


@router.message(Form2.ever_married, F.text.casefold().in_(["да", "нет"]))
async def get_age(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "да":
        await state.update_data(ever_married=1)
    else:
        await state.update_data(ever_married=0)
    await state.set_state(Form2.urban_dweller)
    await message.answer("Вы живёте в городе?", reply_markup=keyboards.survey_kb)


@router.message(Form2.urban_dweller, F.text.casefold().in_(["да", "нет"]))
async def get_age(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "да":
        await state.update_data(urban_dweller=1)
    else:
        await state.update_data(urban_dweller=0)
    await state.update_data(urban_dweller=message.text)
    await state.set_state(Form2.avg_glucose_level)
    await message.answer("Введите Ваш средний уровень глюкозы, если не знаете, то введите 0", reply_markup=keyboards.empty_kb)


@router.message(Form2.avg_glucose_level)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(avg_glucose_level=message.text)
        await state.set_state(Form2.bmi)
        await message.answer("Введите индекс массы тела")
    else:
        await message.answer("Введите заново")


@router.message(Form2.bmi)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(bmi=message.text)
        await state.set_state(Form2.smoking_status)
        await message.answer("Вы курите?", reply_markup=keyboards.smoke_kb)
    else:
        await message.answer("Введите заново")


@router.message(Form2.smoking_status, F.text.casefold().in_(["курю", "курил раньше", "никогда не курил"]))
async def get_age(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "курю":
        await state.update_data(smoking_status=2)
    elif text == "курил раньше":
        await state.update_data(smoking_status=1)
    elif text == "никогда не курил":
        await state.update_data(smoking_status=0)

    key, additional_key = await get_hash(message.from_user.id)
    data = await state.get_data()
    await state.clear()
    data = list(data.values())
    data.append(response)
    data.append(key)
    data.append(additional_key)
    data = tuple(data)
    response = json.loads(RcpClient.call(message, config.first_check_queue))
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute('''UPDATE users SET hypertension = ?,
                    heart_disease = ?,
                    ever_married = ?,
                    urban_dweller = ?,
                    avg_glucose_level = ?,
                    bmi = ?,
                    smoking_status = ?,
                    first_check_result
                    WHERE key = ? AND additional_key = ?''', data)
    users.commit()
    cursor.close()
    users.close()
    
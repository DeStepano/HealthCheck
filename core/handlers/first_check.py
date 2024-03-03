from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards


class Form2(StatesGroup):
    age = State()
    sex = State()
    hypertension = State()
    heart_disease = State()
    ever_married = State()
    urban_dweller = State()
    avg_glucose_level = State()
    bmi = State()
    smoking_status = State()


router = Router()


@router.message(F.text.lower() == "опрос")
async def change_user_data(message: Message, state: FSMContext):
    await state.set_state(Form2.age)
    await message.answer("Введите возраст")


@router.message(Form2.age)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(Form2.sex)
        await message.answer("Введите ваш пол", reply_markup=keyboards.sex_kb)
    else:
        await message.answer("Введите возраст заново")


@router.message(Form2.sex, F.text.casefold().in_(["парень", "девушка"]))
async def get_sex(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(Form2.hypertension)
    await message.answer("Есть ли у Вас гипертония?", reply_markup=keyboards.survey_kb)


@router.message(Form2.hypertension)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(hypertension=message.text)
    await state.set_state(Form2.heart_disease)
    await message.answer("Есть ли у Вас сердечные заболевания?", reply_markup=keyboards.survey_kb)


@router.message(Form2.heart_disease)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(heart_disease=message.text)
    await state.set_state(Form2.ever_married)
    await message.answer("Состояли/состоите ли Вы в браке?", reply_markup=keyboards.delete_kb)


@router.message(Form2.ever_married)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(ever_married=message.text)
    await state.set_state(Form2.urban_dweller)
    await message.answer("Вы живёте в городе?", reply_markup=keyboards.delete_kb)


@router.message(Form2.urban_dweller)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(urban_dweller=message.text)
    await state.set_state(Form2.avg_glucose_level)
    await message.answer("Введите Ваш средний уровень глюкозы, если не знаете, то введите 0")


@router.message(Form2.avg_glucose_level)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(avg_glucose_level=message.text)
        await state.set_state(Form2.bmi)
        await message.answer("Введите индекс массы тела", reply_markup=keyboards.smoke_kb)
    else:
        await message.answer("Введите заново")


@router.message(Form2.bmi)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(bmi=message.text)
        await state.set_state(Form2.smoking_status)
        await message.answer("Вы курите?")
    else:
        await message.answer("Введите заново")


@router.message(Form2.smoking_status)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(smoking_status=message.text)

    data = await state.get_data()
    await state.clear()

    formatted_text = []
    for key, value in data.items():
        formatted_text.append(f"{key}: {value}")

    age, sex, hypertension, heart_disease, ever_married, urban_dweller, avg_glucose_level, bmi, smoking_status = data.values()

    #тут дальше будет что-то разумное, чтобы передать данные алгоритму мл и сохранить в бдшк



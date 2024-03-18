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
    hypertension = State()
    heart_disease = State()
    ever_married = State()
    urban_dweller = State()
    avg_glucose_level = State()
    bmi = State()
    smoking_status = State()


router = Router()


@router.message(Command("Болезнь_3"))
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

    data = await state.get_data()
    await state.clear()

    formatted_text = []
    for key, value in data.items():
        formatted_text.append(f"{key}: {value}")
    print(data)
    hypertension, heart_disease, ever_married, urban_dweller, avg_glucose_level, bmi, smoking_status = data.values()
    await message.answer(f"Тест пройден! Ваши данные: \nГипертнония: {hypertension} \nБолезни сердца: {heart_disease} \nБрак: {ever_married} \nУровень глюкозы: {avg_glucose_level} \nИндекс массы тела: {bmi} \nКурение: {smoking_status}", reply_markup=keyboards.main_kb
                           )
    #тут дальше будет что-то разумное, чтобы передать данные алгоритму мл и сохранить в бдшк



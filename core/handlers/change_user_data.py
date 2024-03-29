from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from aiogram.types import ReplyKeyboardRemove

from core.logic import get_hash

class Form(StatesGroup):
    new_name = State()
    new_age = State()
    new_sex = State()


router = Router()


@router.message(Command("Изменить_данные"), StateFilter(None))
async def change_user_data(message: Message, state: FSMContext):
    await state.set_state(Form.new_name)
    await message.answer("Введите имя", reply_markup=keyboards.empty_kb)


@router.message(Form.new_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.new_age)
    await message.answer("Введите возраст")


@router.message(Form.new_age)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(Form.new_sex)
        await message.answer("Введите ваш пол", reply_markup=keyboards.sex_kb)
    else:
        await message.answer("Введите возраст заново")


@router.message(Form.new_sex, F.text.casefold().in_(["парень", "девушка"]))
async def get_sex(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)

    await message.answer("Данные изменены", reply_markup=keyboards.main_kb)
    data = await state.get_data()
    await state.clear()

    user_id = await get_hash(message.from_user.id)

    formatted_text = []
    for key, value in data.items():
        formatted_text.append(f"{key}: {value}")

    name, age, sex = data.values()
    await message.answer(F" имя: {name} \n возраст: {age} \n пол: {sex}")

    users = sl.connect('core/users.db')
    # id_user = message.from_user.id
    cursor = users.cursor()
    cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
    cursor.execute('UPDATE users SET age = ? WHERE id = ?', (age, user_id))
    cursor.execute('UPDATE users SET sex = ? WHERE id = ?', (sex, user_id))
    users.commit()
    cursor.close()
    users.close()


@router.message(Command("/Главное меню"))
async def insert_main_kb(message: Message):
    message.answer("Главное меню", reply_markup=keyboards.setting_kb)
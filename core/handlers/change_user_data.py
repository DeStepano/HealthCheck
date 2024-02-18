from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards

class Form(StatesGroup):
    name = State()
    age = State()
    sex = State()

router=Router()


@router.message(F.text.lower()=="изменить данные")
async def change_user_data(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Введите имя")

@router.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Введите возраст", reply_markup=keyboards.delete_kb)


@router.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(Form.sex)
        await message.answer("Введите ваш пол", reply_markup=keyboards.sex_kb)
    else:
        await message.answer("Введите возраст заново")


@router.message(Form.sex, F.text.casefold().in_(["парень", "девушка"]))
async def get_sex(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await message.answer("Данные изменены", reply_markup=keyboards.main_kb)
    data = await state.get_data()
    await state.clear()
    
    formatted_text=[]
    for key, value in data.items():
        formatted_text.append(f"{key}: {value}")
    
    name, age, sex = data.values()
    await message.answer(F" имя: {name} \n возраст: {age} \n пол: {sex}")

    users = sl.connect('core/users.db')
    id_user = message.from_user.id
    cursor = users.cursor()
    sqlite_update_query = """Update sqlitedb_developers set name = ?, age = ?, sex = ? where id = ?"""
    column_values = (name, age, sex, id_user)
    cursor.execute(sqlite_update_query, column_values)
    users.commit()
    cursor.close()
    users.close()
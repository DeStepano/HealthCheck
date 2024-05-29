from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl
import hashlib
import asyncio
from core.sql_utils import get_data_by_id, insert_data, insert_array, get_array
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.hash import get_hash

class Form(StatesGroup):
    name = State()
    age = State()
    sex = State()

router=Router()

@router.message(Command("Зарегистрироваться"), StateFilter(None))
async def registration(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Введите имя")


@router.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Введите возраст", reply_markup=keyboards.empty_kb)


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
    await message.answer("Вы зарегестрировались!", reply_markup=keyboards.main_kb)
    data = await state.get_data()
    await state.clear()
    name, age, sex = data.values()
    data = (name, int(age), sex)
    await message.answer(F"имя: {name} \nвозраст: {age} \nпол: {sex}")
    user_id = message.from_user.id
    await insert_data(f'INSERT INTO users (key, additional_key, name, age, sex) VALUES ($1, $2, $3, $4, $5)', data , user_id)
    array = [0]*989
    data = await get_data_by_id("SELECT sex, age FROM users WHERE key = $1 and additional_key = $2", user_id)
    dictionary = {"Парень": 1, "Девушка":0}
    array[-2] = data[1]/110
    array[-1] = dictionary[data[0]]
    await insert_array(array, user_id)
    # print(await get_array(user_id))


@router.message(Form.sex)
async def incorrect_sex(message: Message, state: FSMContext):
    await message.answer("Введите пол заново!", reply_markup=keyboards.sex_kb)

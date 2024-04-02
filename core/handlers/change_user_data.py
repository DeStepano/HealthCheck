from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import asyncio
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.hash import get_hash

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

    key, additional_key = await get_hash(message.from_user.id)
    formatted_text = []
    for key, value in data.items():
        formatted_text.append(f"{key}: {value}")

    name, age, sex = data.values()
    
    await message.answer(F" имя: {name} \nвозраст: {age} \nпол: {sex}")
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute("""UPDATE users SET name = ? WHERE key = ? AND additional_key = ?""", (name, key, additional_key) )
    cursor.execute("""UPDATE users SET age = ? WHERE key = ? AND additional_key = ?""", (age, key, additional_key))
    cursor.execute("""UPDATE users SET sex = ? WHERE key = ? AND additional_key = ?""", (sex, key, additional_key))
    users.commit()
    cursor.close()
    users.close()


@router.message(Command("/Главное меню"))
async def insert_main_kb(message: Message):
    message.answer("Главное меню", reply_markup=keyboards.setting_kb)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.sql_utils import insert_data


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
    user_id = message.from_user.id
    data = await state.get_data()
    name, age, sex = data.values()
    data = (name, int(age), sex)
    await state.clear()
    await insert_data("UPDATE users SET name = $3, age = $4, sex = $5 where key = $1 and additional_key = $2", data, user_id)
    await message.answer("Данные изменены", reply_markup=keyboards.main_kb)


@router.message(Command("/Главное меню"))
async def insert_main_kb(message: Message):
    message.answer("Главное меню", reply_markup=keyboards.setting_kb)
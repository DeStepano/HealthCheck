from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging
import sqlite3 as sl

import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from magic_filter import F
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove,
    CallbackQuery
)


class Form(StatesGroup):
    cp = State()
    trtbps = State()
    chol = State()
    fbs = State()
    restecg = State()
    thalach = State()
    exng = State()
    slope = State()
    ca = State()

router = Router()



class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None
    name: str




def get_keyboard_cp():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Типичная стенокардия", callback_data=NumbersCallbackFactory(action="set_cp", value=0, name = "Типичная стенокардия")
    )
    builder.button(
        text="Атипичная стенокардия", callback_data=NumbersCallbackFactory(action="set_cp", value=1, name = "Атипичная стенокардия" )
    )
    builder.button(
        text="Ангинальная боль", callback_data=NumbersCallbackFactory(action="set_cp", value=2, name = "Ангинальная боль")
    )
    builder.button(
        text="Бессимптомно", callback_data=NumbersCallbackFactory(action="set_cp", value=3, name="Бессимптомно")
    )
    # Выравниваем кнопки по 4 в ряд, чтобы получилось 4 + 1
    builder.adjust(2)
    return builder.as_markup()



def get_keyboard_fbs():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="<120", callback_data=NumbersCallbackFactory(action="set_fbs", value=0, name = "<120")
    )
    builder.button(
        text=">=120", callback_data=NumbersCallbackFactory(action="set_fbs", value=1, name = ">=120" )
    )
    builder.adjust(2)
    return builder.as_markup()



def get_keyboard_restech():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Нормальное", callback_data=NumbersCallbackFactory(action="set_restecg", value=0, name = "Нормальное")
    )
    builder.button(
        text="наличие аномалий ST-T (инверсия зубца Т и/или элевация или депрессия ST > 0,05 мВ)", callback_data=NumbersCallbackFactory(action="set_restecg", value=1, name = "аномалия ST-T" )
    )
    builder.button(
        text="Наличие гипертрофии левого желудочка по критериям Эстеса ", callback_data=NumbersCallbackFactory(action="set_restecg", value=2, name = "гипертрофия желудочка")
    )
    builder.adjust(1)
    return builder.as_markup()



def get_keyboard_exng():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Есть", callback_data=NumbersCallbackFactory(action="set_exng", value=0, name = "Есть")
    )
    builder.button(
        text="Нетю)", callback_data=NumbersCallbackFactory(action="set_exng", value=1, name = "Нетю" )
    )

    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_slope():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Нисходящий", callback_data=NumbersCallbackFactory(action="set_slope", value=0, name = "Нисходящий")
    )
    builder.button(
        text="Плоский", callback_data=NumbersCallbackFactory(action="set_slope", value=1, name = "Плоский" )
    )
    builder.button(
        text="Восходящий", callback_data=NumbersCallbackFactory(action="set_slope", value=2, name = "Восходящий")
    )
    builder.adjust(1)
    return builder.as_markup()




def get_keyboard_ca():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="0", callback_data=NumbersCallbackFactory(action="set_ca", value=0, name = "0")
    )
    builder.button(
        text="1", callback_data=NumbersCallbackFactory(action="set_ca", value=1, name = "1" )
    )
    builder.button(
        text="2", callback_data=NumbersCallbackFactory(action="set_ca", value=2, name = "2")
    )
    builder.button(
        text="3", callback_data=NumbersCallbackFactory(action="set_ca", value=3, name = "3" )
    )
    builder.button(
        text="4", callback_data=NumbersCallbackFactory(action="set_ca", value=4, name = "4")
    )
    builder.adjust(3)
    return builder.as_markup()




@router.message(Command("Болезнь_2"))
async def change_user_data(message: Message, state: FSMContext):
    await state.set_state(Form.cp)
    await message.answer("Как вы бы описали тип боли в груди: Выберете значение:", reply_markup=get_keyboard_cp())


@router.callback_query(NumbersCallbackFactory.filter(F.action == "set_cp"))
async def set_cp(callback: CallbackQuery, callback_data: NumbersCallbackFactory, state: State):
    await state.update_data(cp=callback_data.value)
    await state.set_state(Form.trtbps)
    # await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(f"Как вы бы описали тип боли в груди: {callback_data.name}")
    await callback.message.answer("Введите кровяное давление:")
    # await callback.message.delete()

@router.message(Form.trtbps)
async def set_trtbps(message: Message, state: State):
    if message.text.isdigit():
        await state.update_data(trtbps=int(message.text))
        await state.set_state(Form.chol)
        await message.answer("Холестерин в крови:")
    else:
        message.answer("Введите число заново:")


@router.message(Form.chol)
async def set_trtbps(message: Message, state: State):
    if message.text.isdigit():
        await state.update_data(chol=int(message.text))
        await state.set_state(Form.fbs)
        await message.answer("Уровень сахара в крови натощак:", reply_markup=get_keyboard_fbs())
    else:
        message.answer("Введите число заново:")


@router.callback_query(NumbersCallbackFactory.filter(F.action == "set_fbs"))
async def set_cp(callback: CallbackQuery, callback_data: NumbersCallbackFactory, state: State):
    await state.update_data(fbs=callback_data.value)
    await state.set_state(Form.restecg)
    await callback.message.edit_text(f"Уровень сахара в крови натощак : {callback_data.name}")
    await callback.message.answer("Результаты электрокардиографии в покое:", reply_markup=get_keyboard_restech())

@router.callback_query(NumbersCallbackFactory.filter(F.action == "set_restecg"))
async def set_restecg(callback: CallbackQuery, callback_data: NumbersCallbackFactory, state: State):
    await state.update_data(restecg=callback_data.value)
    await state.set_state(Form.thalach)
    await callback.message.answer("Максимальная частота сердечных сокращений:")


@router.message(Form.thalach)
async def set_trtbps(message: Message, state: State):
    if message.text.isdigit():
        await state.update_data(thalach=int(message.text))
        await state.set_state(Form.exng)
        await message.answer("Стенокардия, вызванная физической нагрузкой:", reply_markup=get_keyboard_exng())
    else:
        message.answer("Введите число заново:")


@router.callback_query(NumbersCallbackFactory.filter(F.action == "set_exng"))
async def set_restecg(callback: CallbackQuery, callback_data: NumbersCallbackFactory, state: State):
    await state.update_data(exng=callback_data.value)
    await state.set_state(Form.slope)
    await callback.message.answer("Наклон пикового сегмента ST при нагрузке:", reply_markup=get_keyboard_slope())


@router.callback_query(NumbersCallbackFactory.filter(F.action == "set_slope"))
async def set_restecg(callback: CallbackQuery, callback_data: NumbersCallbackFactory, state: State):
    await state.update_data(slope=callback_data.value)
    await state.set_state(Form.ca)
    await callback.message.answer("Количество крупных сосудов:", reply_markup=get_keyboard_ca())


@router.callback_query(NumbersCallbackFactory.filter(F.action == "set_ca"))
async def set_restecg(callback: CallbackQuery, callback_data: NumbersCallbackFactory, state: State):
    await state.update_data(slope=callback_data.value)
    data = await state.get_data()
    await state.clear()
    print(data)
    await callback.message.answer("Вы прошли тест!")
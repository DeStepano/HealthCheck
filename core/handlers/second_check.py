from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
import logging
import sqlite3 as sl
import pika
import asyncio
import uuid

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from aiogram.types import ReplyKeyboardRemove
from core.logic import get_hash
from aiogram import F
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


class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n, name):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response


rpc = RpcClient()


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


@router.message(Command("Болезнь_2"), StateFilter(None))
async def change_user_data(message: Message, state: FSMContext):
    await state.set_state(Form.cp)
    await message.answer("Как вы бы описали тип боли в груди: Выберете значение:", reply_markup=keyboards.get_keyboard_cp())


@router.callback_query(keyboards.NumbersCallbackFactory.filter(F.action == "set_cp"))
async def set_cp(callback: CallbackQuery, callback_data: keyboards.NumbersCallbackFactory, state: FSMContext):
    await state.update_data(cp=callback_data.value)
    await state.set_state(Form.trtbps)
    await callback.message.edit_text(f"Как вы бы описали тип боли в груди: {callback_data.name}")
    await callback.message.answer("Введите кровяное давление:")


@router.message(Form.trtbps)
async def set_trtbps(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(trtbps=int(message.text))
        await state.set_state(Form.chol)
        await message.answer("Холестерин в крови:")
    else:
        message.answer("Введите число заново:")


@router.message(Form.chol)
async def set_trtbps(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(chol=int(message.text))
        await state.set_state(Form.fbs)
        await message.answer("Уровень сахара в крови натощак:", reply_markup=keyboards.get_keyboard_fbs())
    else:
        message.answer("Введите число заново:")


@router.callback_query(keyboards.NumbersCallbackFactory.filter(F.action == "set_fbs"), Form.fbs)
async def set_cp(callback: CallbackQuery, callback_data: keyboards.NumbersCallbackFactory, state: State):
    await state.update_data(fbs=callback_data.value)
    await state.set_state(Form.restecg)
    await callback.message.edit_text(f"Уровень сахара в крови натощак : {callback_data.name}")
    await callback.message.answer("Результаты электрокардиографии в покое:", reply_markup=keyboards.get_keyboard_restech())


@router.callback_query(keyboards.NumbersCallbackFactory.filter(F.action == "set_restecg"), Form.restecg)
async def set_restecg(callback: CallbackQuery, callback_data: keyboards.NumbersCallbackFactory, state: FSMContext):
    await state.update_data(restecg=callback_data.value)
    await state.set_state(Form.thalach)
    await callback.message.answer("Максимальная частота сердечных сокращений:")


@router.message(Form.thalach)
async def set_trtbps(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(thalach=int(message.text))
        await state.set_state(Form.exng)
        await message.answer("Стенокардия, вызванная физической нагрузкой:", reply_markup=keyboards.get_keyboard_exng())
    else:
        message.answer("Введите число заново:")


@router.callback_query(keyboards.NumbersCallbackFactory.filter(F.action == "set_exng"), Form.exng)
async def set_restecg(callback: CallbackQuery, callback_data: keyboards.NumbersCallbackFactory, state: FSMContext):
    await state.update_data(exng=callback_data.value)
    await state.set_state(Form.slope)
    await callback.message.answer("Наклон пикового сегмента ST при нагрузке:", reply_markup=keyboards.get_keyboard_slope())


@router.callback_query(keyboards.NumbersCallbackFactory.filter(F.action == "set_slope"), Form.slope)
async def set_restecg(callback: CallbackQuery, callback_data: keyboards.NumbersCallbackFactory, state: FSMContext):
    await state.update_data(slope=callback_data.value)
    await state.set_state(Form.ca)
    await callback.message.answer("Количество крупных сосудов:", reply_markup=keyboards.get_keyboard_ca())


@router.callback_query(keyboards.NumbersCallbackFactory.filter(F.action == "set_ca"), Form.ca)
async def set_restecg(callback: CallbackQuery, callback_data: keyboards.NumbersCallbackFactory, state: FSMContext):
    await state.update_data(ca=callback_data.value)
    data = await state.get_data()
    message = json.dumps(data)
    await callback.message.answer("Начата обработка", reply_markup=keyboards.main_kb)
    response = json.loads(rpc.call(message, 'rpc_queue'))
    data = list(data.values())
    id_user = await get_hash(callback.from_user.id)
    data.append(response)
    data.append(id_user)
    data = tuple(data)
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    cursor.execute('UPDATE users SET cp = ?, trtbps = ?, chol = ?, fbs = ?, restecg = ?, thalach = ?, exng = ?, slope = ?, ca = ?, test1_result = ?  WHERE id = ?', data)
    users.commit()
    cursor.close()
    users.close()

    await state.clear()
    await callback.message.answer(f"Вы прошли тест! Ваши данные:{response}")

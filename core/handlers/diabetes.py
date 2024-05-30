from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
import json
from core.rpc_client import rpcClient
from core.config import config
from core.sql_utils import get_data_by_id, insert_data
from core.states import States


class Form2(StatesGroup):
    hypertension = State()
    heart_disease = State()
    weight = State()
    height = State()
    smoking_status = State()
    HbА1С = State()
    sugar = State()


router = Router()


@router.message(Command("Диабет"), StateFilter(States.check_diseases_command))
async def start_test(message: Message, state: FSMContext):
    await state.set_state(Form2.hypertension)
    await message.answer("Есть ли у Вас гипертония?", reply_markup=keyboards.survey_kb)


@router.message(Form2.hypertension, F.text.casefold().in_(["да", "нет"]))
async def get_hypertension(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "да":
        await state.update_data(hypertension=1)
    else:
        await state.update_data(hypertension=0)
    await state.set_state(Form2.heart_disease)
    await message.answer("Есть или были ли у Вас сердечные заболевания?", reply_markup=keyboards.survey_kb)


@router.message(Form2.heart_disease, F.text.casefold().in_(["да", "нет"]))
async def get_heart_disease(message: Message, state: FSMContext):
    text =  message.text.lower()
    if text == "да":
        await state.update_data(heart_disease=1)
    else:
        await state.update_data(heart_disease=0)
    await state.set_state(Form2.weight)
    await message.answer("Введите ваш вес", reply_markup=keyboards.empty_kb)


@router.message(Form2.weight)
async def get_weight(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(weight=int(message.text))
        await state.set_state(Form2.height)
        await message.answer("Введите ваш рост")
    else:
        await message.answer("Введите число")


@router.message(Form2.height)
async def get_weight(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(height=int(message.text))
        await state.set_state(Form2.smoking_status)
        await message.answer("Вы курите?", reply_markup=keyboards.smoke_kb)
    else:
        await message.answer("Введите число")


@router.message(Form2.smoking_status, F.text.casefold().in_(["курю", "курил раньше", "никогда не курил", "когда либо", "бросаю"]))
async def get_smoking_status(message: Message, state: FSMContext):
    ans = {"курю": 1, "курил раньше": 3, "никогда не курил": 4, "когда либо": 0, "бросаю": 2}
    await state.update_data(smoking_status = ans[str(message.text).casefold()])
    await state.set_state(Form2.HbА1С)
    await message.answer("Введте значение HbА1С")


@router.message(Form2.HbА1С)
async def get_HbA1C(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(HbА1С=int(message.text))
        await state.set_state(Form2.sugar)
        await message.answer("Ведите уровень сахара в крови")
    else:
        await message.answer("Введите число")


@router.message(Form2.sugar)
async def get_sugar(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(sugar=int(message.text))
        data = await state.get_data()
        age = await get_data_by_id("SELECT age FROM users WHERE key = $1 AND additional_key = $2", message.from_user.id)
        gender = await get_data_by_id("SELECT sex FROM users WHERE key = $1 AND additional_key = $2", message.from_user.id)
        await insert_data("UPDATE users SET hypertension = $3, heart_disease = $4, bmi = $5, smoking_status = $6, HbА1С = $7, sugar = $8 WHERE key = $1 AND additional_key = $2", (data['hypertension'], data['heart_disease'], data['smoking_status'], data['weight']/(data['height']/100)**2, data['HbА1С'], data['sugar']), message.from_user.id)
        if gender[0]=="Парень":
            gender = 1
        else:
            gender = 0
        data = [[age[0], gender ,data['hypertension'], data['heart_disease'], data['smoking_status'], data['weight']/(data['height']/100)**2, data['HbА1С'], data['sugar']]]
        await state.clear()
        data = json.dumps(data)
        await message.answer("Начат анализ")
        response = json.loads(rpcClient.call(data, config.first_check_queue))
        await insert_data('UPDATE users SET first_check_result = $3 WHERE key = $1 AND additional_key = $2', (response,), message.from_user.id)
        await message.answer(f"Ваш результат: {response}", reply_markup=keyboards.diagnostic_kb)
    else:
        await message.answer("Введите число")


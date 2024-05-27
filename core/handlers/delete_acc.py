from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards
from core.hash import get_hash
from core.sql_utils import check_data, delete_user, get_data_by_id

router = Router()

@router.message(Command("Удалить_аккаунт"))
async def change_user_data(message: Message, state: FSMContext):
    await message.answer("Вы уверены?", reply_markup=keyboards.delete_kb)


@router.message(Command("Точно_удалить"))
async def change_user_data(message: Message, state: FSMContext):
    user_id = message.from_user.id
    brain_image = await check_data("SELECT brain_image FROM users WHERE key = $1 AND additional_key = $2", user_id)
    xray_image = await check_data("SELECT xray_image FROM users WHERE key = $1 AND additional_key = $2", user_id)
    if brain_image:
        path_brain_image = await get_data_by_id("SELECT brain_image FROM users WHERE key = $1 AND additional_key = $2", user_id)
        os.remove(f"{path_brain_image[0]}")
    if xray_image:
        path_xray_image = await get_data_by_id("SELECT xray_image FROM users WHERE key = $1 AND additional_key = $2", user_id)
        os.remove(f"{path_xray_image[0]}")
    await delete_user(user_id)
    await message.answer("Успешно", reply_markup=keyboards.registration_kb)


@router.message(Command("Не_удалять"))
async def change_user_data(message: Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=keyboards.setting_kb)

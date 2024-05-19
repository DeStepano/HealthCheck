from aiogram.fsm.context import FSMContext
import sqlite3 as sl
import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards import keyboards
from core.hash import get_hash


router = Router()

names = ("brain_result", "xray_result", "first_check_result", "second_check_result")


@router.message(Command("Мои_анализы"))
async def show_test_results(message: Message):
    keys = await get_hash(message.from_user.id)
    print(keys)
    users = sl.connect('core/users.db')
    cursor = users.cursor()
    data = cursor.execute("""SELECT brain_result, xray_result, first_check_result, second_check_result FROM users WHERE key = ? AND additional_key = ?""", keys).fetchone()
    cursor.close()
    users.close()
    results = []

    for i in range(0, len(data)):
        if not (data[i] is None):
            results.append(str(names[i]) + ': ' + str(data[i]))
    
    text = "Ваши анализы: "

    if(len(results) == 0):
        text = "Вы не проходили обследований"
    else:
        for i in results:
            text = text + '\n' + i
    
    await message.answer(text=text)
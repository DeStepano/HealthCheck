from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from core.sql_utils import get_data_by_id


router = Router()


names = ("МРТ", "Пневмония", "Диабет", "Полная проверка")


@router.message(Command("Мои_анализы"))
async def show_test_results(message: Message):
    user_id = message.from_user.id
    data = await get_data_by_id("SELECT brain_result, xray_result, first_check_result, fullcheck_result FROM users WHERE key = $1 AND additional_key = $2", user_id)
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
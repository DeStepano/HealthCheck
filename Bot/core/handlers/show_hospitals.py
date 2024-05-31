from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.states import States
from core.keyboards import keyboards


router = Router()


@router.message(Command("Пневмония"), StateFilter(States.show_hospitals_command))
async def show_pneumonia(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Больницы, занимающиеся лечением пневмонии", reply_markup=keyboards.web_kb_pneumonia)


@router.message(Command("Диабет"), StateFilter(States.show_hospitals_command))
async def show_diabetes(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Больницы, занимающиеся лечением диабета", reply_markup=keyboards.web_kb_diabetes)


@router.message(Command("ВИЧ"), StateFilter(States.show_hospitals_command))
async def show_hiv(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Больницы, занимающиеся лечением вич", reply_markup=keyboards.web_kb_hiv)


@router.message(Command("Ларингит"), StateFilter(States.show_hospitals_command))
async def show_laryngitis(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Больницы, занимающиеся лечением ларингита", reply_markup=keyboards.web_kb_acute_laryngitis)


@router.message(Command("Глиома"), StateFilter(States.show_hospitals_command))
async def show_hiv(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Больницы, занимающиеся лечением глиомы", reply_markup=keyboards.web_kb_glioma)


@router.message(Command("Менингиома"), StateFilter(States.show_hospitals_command))
async def show_laryngitis(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Больницы, занимающиеся лечением менингиомы", reply_markup=keyboards.web_kb_meningioma)
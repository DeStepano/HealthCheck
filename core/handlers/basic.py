from aiogram import Bot
from aiogram.types import Message
from config import all_users

async def start(message: Message , bot: Bot):
    if message.from_user.id not in all_users.keys():
        all_users[message.from_user.id] = [message.from_user.first_name, message.from_user.full_name]
    await message.answer('Привет! Я бот, помогающий выявлять заболевания по твоим анализам. Давай познакомимся! Отправь, пожалуйста, свое имя и фамилию в формате: "Имя Фамилия."')
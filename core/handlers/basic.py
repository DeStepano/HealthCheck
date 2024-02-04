from aiogram import Bot
from aiogram.types import Message

async def start(message: Message , bot: Bot):
    await message.answer('Привет! Я бот, помогающий выявлять заболевания по твоим анализам. Давай познакомимся! Отправь, пожалуйста, свое имя и фамилию в формате: "Имя Фамилия."')
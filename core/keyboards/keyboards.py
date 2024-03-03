from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)

registration_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/Зарегистрироваться"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/Проверить_анализы"),
            KeyboardButton(text="/Диалог_с_врачем")
        ],
        [
            KeyboardButton(text="/Мои_анализы"),
            KeyboardButton(text="/Настройки")
        ],
        
    ],
    resize_keyboard=True
)

diagnostic_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/Болезнь_1"),
            KeyboardButton(text="/Болезнь_2")
        ],
        [
            KeyboardButton(text="/Болезнь_3"),
            KeyboardButton(text="/Болезнь_4")
        ],
        [
            KeyboardButton(text="/Главное_меню")
        ]
    ],
    resize_keyboard=True
)

smoke_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Курю"),
            KeyboardButton(text="Курил раньше"),
            KeyboardButton(text="Никогда не курил")
        ],
    ],
    resize_keyboard=True
)

survey_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Есть"),
            KeyboardButton(text="Нет")
        ],
    ],
    resize_keyboard=True
)


setting_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/Удалить_аккаунт"),
            KeyboardButton(text="/Изменить_данные")
        ],
        [
            KeyboardButton(text="/Главное_меню")
        ]
    ],
    resize_keyboard=True
)



delete_kb=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/Точно_удалить"),
            KeyboardButton(text="/Не_удалять")
        ]
    ]
)

sex_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Парень"),
            KeyboardButton(text="Девушка")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

empty_kb = ReplyKeyboardRemove()



from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType
)






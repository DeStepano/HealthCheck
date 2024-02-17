from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType
)

registration_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зарегистрироваться"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Проверить анализы"),
            KeyboardButton(text="Диалог с врачем")
        ],
        [
            KeyboardButton(text="Мои анализы"),
            KeyboardButton(text="Настройки")
        ]
    ],
    resize_keyboard=True
)

delete_kb=ReplyKeyboardMarkup(
    keyboard=[
        []
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
from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)
from magic_filter import F
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
            KeyboardButton(text="/Флюорография")
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
            KeyboardButton(text="Да"),
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


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None
    name: str


def get_keyboard_cp():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Типичная стенокардия", callback_data=NumbersCallbackFactory(action="set_cp", value=0, name = "Типичная стенокардия")
    )
    builder.button(
        text="Атипичная стенокардия", callback_data=NumbersCallbackFactory(action="set_cp", value=1, name = "Атипичная стенокардия" )
    )
    builder.button(
        text="Ангинальная боль", callback_data=NumbersCallbackFactory(action="set_cp", value=2, name = "Ангинальная боль")
    )
    builder.button(
        text="Бессимптомно", callback_data=NumbersCallbackFactory(action="set_cp", value=3, name="Бессимптомно")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_keyboard_fbs():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="<120", callback_data=NumbersCallbackFactory(action="set_fbs", value=0, name = "<120")
    )
    builder.button(
        text=">=120", callback_data=NumbersCallbackFactory(action="set_fbs", value=1, name = ">=120" )
    )
    builder.adjust(2)
    return builder.as_markup()


def get_keyboard_restech():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Нормальное", callback_data=NumbersCallbackFactory(action="set_restecg", value=0, name = "Нормальное")
    )
    builder.button(
        text="наличие аномалий ST-T (инверсия зубца Т и/или элевация или депрессия ST > 0,05 мВ)", callback_data=NumbersCallbackFactory(action="set_restecg", value=1, name = "аномалия ST-T" )
    )
    builder.button(
        text="Наличие гипертрофии левого желудочка по критериям Эстеса ", callback_data=NumbersCallbackFactory(action="set_restecg", value=2, name = "гипертрофия желудочка")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_exng():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Есть", callback_data=NumbersCallbackFactory(action="set_exng", value=0, name = "Есть")
    )
    builder.button(
        text="Нет", callback_data=NumbersCallbackFactory(action="set_exng", value=1, name = "Нет" )
    )

    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_slope():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Нисходящий", callback_data=NumbersCallbackFactory(action="set_slope", value=0, name = "Нисходящий")
    )
    builder.button(
        text="Плоский", callback_data=NumbersCallbackFactory(action="set_slope", value=1, name = "Плоский" )
    )
    builder.button(
        text="Восходящий", callback_data=NumbersCallbackFactory(action="set_slope", value=2, name = "Восходящий")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_ca():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="0", callback_data=NumbersCallbackFactory(action="set_ca", value=0, name = "0")
    )
    builder.button(
        text="1", callback_data=NumbersCallbackFactory(action="set_ca", value=1, name = "1" )
    )
    builder.button(
        text="2", callback_data=NumbersCallbackFactory(action="set_ca", value=2, name = "2")
    )
    builder.button(
        text="3", callback_data=NumbersCallbackFactory(action="set_ca", value=3, name = "3" )
    )
    builder.button(
        text="4", callback_data=NumbersCallbackFactory(action="set_ca", value=4, name = "4")
    )
    builder.adjust(3)
    return builder.as_markup()


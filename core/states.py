from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    show_hospitals_command = State()
    check_diseases_command = State()
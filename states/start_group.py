from aiogram.fsm.state import State, StatesGroup


class startSG(StatesGroup):
    start = State()
    generates = State()
    chose_generates = State()
    generate = State()
    generate_2 = State()
    ref_program = State()
    success_payment = State()
    unsuccess_payment = State()
    success_generate = State()


class adminSG(StatesGroup):
    start = State()
    malling = State()
    accept = State()

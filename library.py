from aiogram.fsm.state import StatesGroup, State


class PowerBank(StatesGroup):
    choosing_capacity = State()
    choosing_QC = State()
    choosing_QC_save = State()
    choosing_capacity_phone = State()
    final_calc = State()

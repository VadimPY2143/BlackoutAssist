import asyncio
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F, Router
from aiogram.dispatcher import router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message, \
    ReplyKeyboardRemove
import asyncio
from constt import TOKEN
import datetime
from library import PowerBank

EFFICIENCY = 0.85

AMPERAGE_FASTCHARGE = 9

AMPERAGE_REAL = 5

AMPERAGE = 3.7

bot = Bot(token=TOKEN)
dp = Dispatcher()
form_router = Router()
dp.include_router(form_router)

inline_kb_menu = [
    [InlineKeyboardButton(text="Powerbank", callback_data="power")],
    [InlineKeyboardButton(text="Powerbank PD", callback_data="power_pd")],
    [InlineKeyboardButton(text="Charging station", callback_data="charg_st")],
    [InlineKeyboardButton(text="UPS", callback_data="ups")]
]

main_kb_menu = InlineKeyboardMarkup(inline_keyboard=inline_kb_menu)


@form_router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f'Привіт {message.from_user.first_name}\nВітаємо вас у <b>BlackoutAssistBot</b>\nЦей бот допоможе вам підібрати зарядний пристрій',
        parse_mode='html', reply_markup=main_kb_menu)
    print("User: ", message.from_user.username)


"""
Додаємо стейтмашину поверббанк
"""


@form_router.callback_query(F.data == "power")
async def power_start(message: Message, state: FSMContext):
    await state.set_state(PowerBank.choosing_capacity)
    await bot.send_message(message.from_user.id, 'Яка ємність павербанку?')


@form_router.message(PowerBank.choosing_capacity)
async def set_powerbank_capacity(message: Message, state: FSMContext):
    try:
        capacity_int = int(message.text)
        print("Введено Powerbank ємністю", capacity_int)
        await state.update_data(choosing_capacity=capacity_int)
        await message.answer(f'Ви ввели {capacity_int}. Усе вірно? \nДля пітвердження введіть що завгодно')

        await state.set_state(PowerBank.choosing_QC)

    except (TypeError, ValueError):
        await message.answer('Введіть коректну ємність?')
        await message.answer('Яка ємність павербанку?')
        await state.set_state(PowerBank.choosing_capacity)


@form_router.message(PowerBank.choosing_QC)
async def set_powerbank_qc(message: Message, state: FSMContext):
    await state.set_state(PowerBank.choosing_QC_save)
    await message.answer(
        "Чи підтримує телефон Quick Charge \n(Павербанк з робочою потужністю до 100W, USB-PD дозволяє заряджати навіть великі пристрої, такі як планшети і ноутбуки)?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Так є QC"),
                    KeyboardButton(text="Ні немає QC"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(PowerBank.choosing_QC_save, F.text.casefold() == "так є qc")
async def process_pd_yes(message: Message, state: FSMContext) -> None:
    await state.update_data(choosing_QC=True)
    await message.reply(
        "Введіть ємність акумулятору телефону:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(PowerBank.choosing_capacity_phone)


@form_router.message(PowerBank.choosing_QC_save, F.text.casefold() == "ні немає qc")
async def process_pd_not(message: Message, state: FSMContext) -> None:
    await state.update_data(choosing_QC=False)
    await message.answer(
        "Введіть ємність акумулятору телефону:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(PowerBank.choosing_capacity_phone)


@form_router.message(PowerBank.choosing_capacity_phone)
async def process_capacity_phone(message: Message, state: FSMContext) -> None:
    try:
        capacity_phone_int = int(message.text)
        print("Введено телефон ємністю", capacity_phone_int)
        data2 = await state.update_data(choosing_capacity_phone=capacity_phone_int)
        await state.set_state(PowerBank.final_calc)
        await state.clear()
    except (TypeError, ValueError):
        await message.answer('Введіть коректну ємність?')
        await message.answer('Яка ємність акумулятора телефону?')
        await state.set_state(PowerBank.choosing_capacity)
    await show_summary_pb(message=message, data=data2)


async def show_summary_pb(message: Message, data: Dict[str, Any]) -> None:
    choosing_capacity = data["choosing_capacity"]
    choosing_qc = data["choosing_QC"]
    choosing_capacity_phone = data["choosing_capacity_phone"]
    wt_hour = choosing_capacity / 1000 * AMPERAGE
    real_capacity = choosing_capacity * AMPERAGE / AMPERAGE_REAL * EFFICIENCY
    real_capacity_fastcharge = choosing_capacity * AMPERAGE / AMPERAGE_FASTCHARGE * EFFICIENCY
    number_of_charges = real_capacity / choosing_capacity_phone
    number_of_charges_fastcharge = real_capacity_fastcharge / choosing_capacity_phone
    text = f"<b>Павербанк з заявленою ємністю {choosing_capacity} мАч(міліампер-часів) </b> <b>Насправді має" \
           f" ємність приблизно {real_capacity} мАч</b>\n" \
           f"При заряджанні телефону з швидкою зарядкою ємність буде ще меншою і " \
           f"складатиме {real_capacity_fastcharge}, " \
           f"що у Ватт-годинах складає {wt_hour}Вт\n" \
           f"Тому повербанк зможе зарядити ваш телефон {number_of_charges} разів у звичайному режимі" \
           f" та {number_of_charges_fastcharge} разів у режимі швидкої зарядки\n" \
           f"<b>Дякуємо, що користуєтесь нашим ботом</b>\n" \
           f"<b>Щоб почати спочатку введіть команду /start</b>"
    await message.answer(text=text, parse_mode='html', reply_markup=ReplyKeyboardRemove())


"""
Стейтмашина поверббанк кінець блоку
"""


@form_router.callback_query(F.data == "power_pd")
async def power_pd_start(callback: Message):
    await callback.message.answer("Ви вибрали повербанк ПД")


@form_router.callback_query(F.data == 'charg_st')
async def charge_station_start(callback: Message):
    await callback.message.answer('Ви вибрали зарядну станцію')


@form_router.callback_query(F.data == 'ups')
async def UPS_start(callback: Message):
    await callback.message.answer('Ви вибрали ДБЖ')


async def main():
    await dp.start_polling(bot)


"""
Додаємо вивід часу запуску боту
"""
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print('Bot started successful at', formatted_datetime)

if __name__ == '__main__':
    asyncio.run(main())

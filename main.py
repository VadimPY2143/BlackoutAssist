import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
import asyncio
from constt import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


inline_kb_menu = [
    [InlineKeyboardButton(text="Powerbank", callback_data="power")],
    [InlineKeyboardButton(text="Powerbank PD", callback_data="power_pd")],
    [InlineKeyboardButton(text="Charging station", callback_data="charg_st")],
    [InlineKeyboardButton(text="UPS", callback_data="ups")]
]


main_kb_menu = InlineKeyboardMarkup(inline_keyboard=inline_kb_menu)


@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(f"Привіт {message.from_user.first_name}\nВітаємо вас у <b>BlackoutAssistBot</b>\nЦей бот допоможе вам підібрати зарядний пристрій", parse_mode="html", reply_markup=main_kb_menu)


@dp.callback_query(F.data == "power")
async def power_start(callback: Message):
    await callback.message.answer("Ви вибрали повербанк")

@dp.callback_query(F.data == "power_pd")
async def power_pd_start(callback: Message):
    await callback.message.answer("Ви вибрали повербанк ПД")


@dp.callback_query(F.data == 'charg_st')
async def charge_station_start(callback: Message):
    await callback.message.answer('Ви вибрали зарядну станцію')


@dp.callback_query(F.data == 'ups')
async def UPS_start(callback: Message):
    await callback.message.answer('Ви вибрали ДБЖ')



async def main():
    await dp.start_polling(bot)
print("Запущено")


if __name__ == "__main__":
    asyncio.run(main())
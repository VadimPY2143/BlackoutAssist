import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
import asyncio
from constt import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


inline_kb_menu = [
    [InlineKeyboardButton(text='Powerbank', callback_data='power')]
]


main_kb_menu = InlineKeyboardMarkup(inline_keyboard=inline_kb_menu)


@dp.message(F.text == '/start')
async def start(message: Message):
    await message.answer(f'Привіт {message.from_user.first_name}\nВітаємо вас у <b>BlackoutAssistBot</b>\nЦей бот допоможе вам підібрати зарядний пристрій', parse_mode='html', reply_markup=main_kb_menu)


@dp.callback_query(F.data == 'power')
async def power_start(callback: Message):
    await callback.message.answer('Ви вибрали повербанк')



async def main():
    await dp.start_polling(bot)
print('Запущено')

print("Hello Vadim")


if __name__ == '__main__':
    asyncio.run(main())
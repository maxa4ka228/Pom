from env import TOKEN #Импортирую токен, чтобы его никто не украл)
from aiogram import Bot, Dispatcher, executor, types# Ссылка на бота в телеграмме -> https://t.me/Pon228723_bot
from aiogram.dispatcher.filters import Text # Ссылка на бота http://qrcoder.ru/code/?https%3A%2F%2Ft.me%2FPon228723_bot&4&0
import time#Импортирую время для того, чтобы человек подумал, что робот долго думает и пользователь мог прочитать, что написал бот комфортно

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Включить"]
    keyboard.add(*buttons)
    await message.answer("Алл", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Включить"))
    async def with_puree(message: types.Message):
        for i in range(100):
            await message.answer("🥶")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

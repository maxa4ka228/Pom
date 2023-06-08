from env import TOKEN #Импортирую токен, чтобы его никто не украл)
import logging

from aiogram import Bot, Dispatcher, executor, types

# print(aiogramm.__version__)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ первый бот Алексей!\nНапиши мне и я повторю за тобой и напишу твой имя ;)")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text + f", {message.from_user['username']}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

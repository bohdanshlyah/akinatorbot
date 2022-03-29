# import akinator
# import asyncio
import logging
import os


from aiogram import Bot, Dispatcher, executor, types
# from akinator.async_aki import Akinator
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Start Game")
    keyboard.add(button_1)
    await message.reply("Hi!\nI'm AkinatorBot!", reply_markup=keyboard)

@dp.message_handler(text=("Start Game"))
async def start_game(message: types.Message):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Game started!", reply_markup=keyboard)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Yes', 'No', 'I don\'t know', 'Probably', 'Probably not', 'Go Back!']
    keyboard.add(*buttons)
    await message.answer("First question", reply_markup=keyboard)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
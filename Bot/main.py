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

    await message.reply("Hi!\nI'm AkinatorBot!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
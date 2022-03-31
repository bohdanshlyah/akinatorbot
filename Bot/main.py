import akinator
import logging
import time


from aiogram import Bot, Dispatcher, executor, types
from akinator.async_aki import Akinator
from config import TOKEN
API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
aki = Akinator()
language = None


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Start Game")
    keyboard.add(button_1)
    await message.answer("Hi!\nI'm AkinatorBot!", reply_markup=keyboard)


@dp.message_handler(commands=["en", "en_animals", "ar", "cn", "de", "de_animals", "es", "es_animals", "fr", "fr_animals", "fr_objects", "il", "it", 
            "it_animals", "jp", "jp_animals", "kr", "nl", "pl", "pt", "ru", "tr", "id"])
async def change_langeage(message: types.Message):
    global language
    language = message.text[1:]
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Language changed!", reply_markup=keyboard)
    await aki.close()
    time.sleep(1)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Restart Game")
    keyboard.add(button_1)
    await message.answer("Please restart game!", reply_markup=keyboard)


@dp.message_handler(text=('Yes', 'No', 'I don\'t know', 'Probably', 'Probably not', 'Go Back!', 
'yes', 'y', '0', 'no', 'n', '1', 'i', 'idk', 'i dont know', '2', 'p', '3', 'pn', '4'))
async def answer_handler(message: types.Message):
    if aki.progression <= 80:
        if message.text == "Go Back!":
            try:
                q = await aki.back()
                await message.answer(q)
            except akinator.CantGoBackAnyFurther:
                await message.answer("Can`t go back anymore!")
        else:
            q = await aki.answer(message.text)
            await message.answer(q)
    else:
        await aki.win()
        await message.answer_photo('https://www.pinterest.com/pin/540783867729782893/')
        keyboard = types.ReplyKeyboardRemove()
        await message.answer(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})!", reply_markup=keyboard)
        await message.answer_photo(f"{aki.first_guess['absolute_picture_path']}")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Yeah, You are right', 'No, You are wrong']
        keyboard.add(*buttons)
        await message.answer(f"Was I correct?", reply_markup=keyboard)


@dp.message_handler(text=('Yeah, You are right', 'No, You are wrong'))
async def win_handler(message: types.Message):
    keyboard = types.ReplyKeyboardRemove()
    if message.text == 'Yeah, You are right':
        await message.answer("Yay, I won!", reply_markup=keyboard)
        await message.answer_photo("https://www.pinterest.com/pin/243968504786224653/")
    else:
        await message.answer("Bravo, You have defeated Me", reply_markup=keyboard)
        await message.answer_photo("https://www.pinterest.com/pin/576249714797127279/")

    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Start Game")
    keyboard.add(button_1)
    await message.answer("Wanna play again?", reply_markup=keyboard)
    await aki.close()

@dp.message_handler(text=("Start Game", "Restart Game"))
async def start_game(message: types.Message):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Game started!", reply_markup=keyboard)
    await message.answer_photo("https://www.pinterest.com/pin/504121752013880224/")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Yes', 'No', 'I don\'t know', 'Probably', 'Probably not', 'Go Back!']
    keyboard.add(*buttons)
    await message.answer("First question!", reply_markup=keyboard)
    try:
        q = await aki.start_game(language=language)
    except:
        print("ERROR!!!!")
        await aki.close()
        time.sleep(1)
        q = await aki.start_game(language=language)
    await message.answer(q)


@dp.message_handler()
async def another_text(message: types.Message):
    await message.answer("Please answer like that:")
    await message.answer(
        """- "Yes" OR "y" OR "0" for YES
- "No" OR "n" OR "1" for NO
- "I don't know" OR "idk" OR "i dont know" OR "i" OR "2" for I DON'T KNOW
- "Probably" OR "p" OR "3" for PROBABLY
- "Probably not" OR "pn" OR "4" for PROBABLY NOT""")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
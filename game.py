import aiogram
import sqlite3
import time
from function import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

kb1 = InlineKeyboardMarkup(row_width=1)
b1 = InlineKeyboardButton(text="Приєднатись", url="https://t.me/BunkerTheBoardGameBot")
kb1.add(b1)

TOKEN = "5635838800:AAGMT6Tw1j0Nzbdwlz3adgiFYVhgQQtGSeM"

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["game"])
async def game(message: types.Message):
    await message.answer(text=f'Приєднуйся до гри в бункер!\n\nГравці:\n\n', reply_markup=kb1)

@dp.message_handler(commands=['join'])
async def join(message: types.message):
    
    # підключення файлу з базою даних

    connect = sqlite3.connect('players.db')
    cursor = connect.cursor()

    # створення таблиць в базі даних

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER UNIQUE,
        name TEXT UNIQUE,
        CONSTRAINT player_unique UNIQUE (id, name)
    )""")

    connect.commit()

    user_name = message.from_user.username
    user_id = message.chat.id
    info = cursor.execute(f'SELECT id FROM login_id WHERE id={user_id}')
    if info.fetchone() is None:
        cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")
        cursor.execute(f"SELECT name FROM login_id WHERE name = '{user_name}'")
        cursor.execute("INSERT INTO login_id VALUES(?, ?)", (user_id, user_name))
        connect.commit()
        await message.answer(message.chat.id, f'Ти приєднався до гри!')
    else:
        await message.answer(message.chat.id, 'Ти вже у грі!')

if __name__ == '__main__':
    executor.start_polling(dp)


print("hello")
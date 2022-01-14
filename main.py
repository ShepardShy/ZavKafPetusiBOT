from aiogram import Bot, Dispatcher, executor, types
from database_connector import DbConnector
import os
import logging
import random

format_log = "%(asctime)s: %(message)s"
logging.basicConfig(format=format_log, level=logging.INFO,
                    datefmt="%H:%M:%S")

token = os.getenv("TOKEN")
if not token:
    exit("Error: not find environment variable 'TOKEN'")

bot = Bot(token=token)
dispatcher = Dispatcher(bot)

db = DbConnector()


@dispatcher.message_handler(commands=['start', 'help'])
async def process_start(message: types.Message):
    response = """Привет! Бот активен!\n
    Доступные команды:\n
    /govno - возвращает рандомного говно-кодера
    """
    await message.answer(response)


@dispatcher.message_handler(commands=['govno'])
async def random_coder(message: types.Message):
    all_coders = db.select_all_coders()
    idx = random.randint(0, len(all_coders) - 1)
    res = all_coders[idx][2]
    await message.answer(res)


def start_bot():
    db.start_init()
    executor.start_polling(dispatcher=dispatcher)


if __name__ == "main":
    start_bot()

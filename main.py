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

@dispatcher.message_handler(commands=['ETS2'])
async def russian_roulette(message: types.Message):
    first_coder = random_coder()
    second_coder = random_coder()
    #Проверяем не стреляется ли человек сам с собой
    if (first_coder == second_coder):
        while (first_coder == second_coder):
            second_coder = random_coder()
    else:
        await message.answer("Игроки ", first_coder, " и ", second_coder, " решили испытать удачу и запустили евро трак симулятор")
        #выстрел первого игрока
        bullet = random.randint(0, 6)
        if (bullet == 3):
            answer_fail(first_coder)
        else:
            answer_success(first_coder)
        #выстрел второго игрока
        bullet = random.randint(0, 6)
        if (bullet == 3):
            answer_fail(second_coder)
        else:
            answer_success(first_coder)

def start_bot():
    db.start_init()
    executor.start_polling(dispatcher=dispatcher)


if __name__ == "__main__":
    start_bot()

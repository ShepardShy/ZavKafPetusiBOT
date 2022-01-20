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

#Получение списка комманд для бота
@dispatcher.message_handler(commands=['start', 'help'])
async def process_start(message: types.Message):
    response = """Привет! Бот активен!\n
    Доступные команды:\n
    /govno - возвращает рандомного говно-кодера\n
    /ETS2 - устраивает русскую рулетку между двумя случайными говно-кодерами
    """
    await message.answer(response)

#Получаем данные о случайном говнокодере
def random_coder():
    all_coders = db.select_all_coders()
    idx = random.randint(0, len(all_coders) - 1)
    coder = all_coders[idx]
    return coder

#Вывод случайного говнокодера
@dispatcher.message_handler(commands=['govno'])
async def call_random_coder(message: types.Message):
    await message.answer(random_coder()[2])

#Русская рулетка
@dispatcher.message_handler(commands=['ETS2'])
async def russian_roulette(message: types.Message):
    first_coder = random_coder()[1]
    second_coder = random_coder()[1]
    first_coder_shot = False
    second_coder_shot = False
    #Проверяем не стреляется ли человек сам с собой
    if (first_coder == second_coder):
        while (first_coder == second_coder):
            second_coder = random_coder()[1]
    else:
        await message.answer("Игроки ", first_coder, " и ", second_coder, " решили испытать удачу и запустили Euro Truck Simulator 2")
        #Выстрел первого игрока
        bullet = random.randint(0, 6)
        if (bullet == 3):
            await message.answer(db.answer_fail(first_coder))
            first_coder_shot = True
        else:
            await message.answer(db.answer_success(first_coder))
        #Выстрел второго игрока
        bullet = random.randint(0, 6)
        if (bullet == 3):
            await message.answer(db.answer_fail(second_coder))
            second_coder_shot = True
        else:
            await message.answer(db.answer_success(second_coder))
        #Вывод победителя
        if ((first_coder_shot == False) and (second_coder_shot == False)):
            await message.answer("Победителя нет, оба продолжили свой путь ниндзя в аудитории")
        if ((first_coder_shot == False) and (second_coder_shot == True)):
            await message.answer("Победитель: ", first_coder)
        if ((first_coder_shot == True) and (second_coder_shot == False)):
            await message.answer("Победитель: ", second_coder)
        if ((first_coder_shot == True) and (second_coder_shot == True)):
            await message.answer("Победителя нет, оба пошли играть в комнату")

def start_bot():
    db.start_init()
    executor.start_polling(dispatcher=dispatcher)


if __name__ == "__main__":
    start_bot()
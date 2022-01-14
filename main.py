from aiogram import Bot, Dispatcher, executor, types
import os
import logging

format_log = "%(asctime)s: %(message)s"
logging.basicConfig(format=format_log, level=logging.INFO,
                    datefmt="%H:%M:%S")

token = os.getenv("TOKEN")
if not token:
    exit("Error: not find environment variable 'TOKEN'")

bot = Bot(token=token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start', 'help'])
async def process_start(message: types.Message):
    response = """Привет! Бот активен!\n
    Доступные команды:\n
    
    """
    await message.answer(response)


def start_bot():
    executor.start_polling(dispatcher=dispatcher)


if __name__ == "main":
    start_bot()

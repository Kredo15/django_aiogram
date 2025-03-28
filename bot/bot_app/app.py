from aiogram import Bot, Dispatcher
import os


API_KEY_BOT = os.getenv('API_KEY_BOT')
bot = Bot(token=API_KEY_BOT)
dp = Dispatcher()

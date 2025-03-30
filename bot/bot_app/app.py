from aiogram import Bot, Dispatcher
import os
from aiogram.fsm.storage.redis import RedisStorage
from .local_settings import REDIS_URL


API_KEY_BOT = os.getenv('API_KEY_BOT')
storage = RedisStorage.from_url(REDIS_URL)
bot = Bot(token=API_KEY_BOT)
dp = Dispatcher(storage=storage)

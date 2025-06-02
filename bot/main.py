from dotenv import load_dotenv

load_dotenv()

from bot_app.app import dp, bot


if __name__ == "__main__":
    dp.run_polling(bot)

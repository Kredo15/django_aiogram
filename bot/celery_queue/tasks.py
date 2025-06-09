import os
from dotenv import load_dotenv

load_dotenv()

from celery import Celery
import asyncio
from celery.schedules import crontab
from bot_app.app import bot
from bot_app.data_fetcher import get_user_for_activity


app_celery = Celery('tasks',
                    broker=os.getenv('CELERY_BROKER'),
                    backend=os.getenv('CELERY_BACKEND'),
                    include=['celery_queue.tasks'])


@app_celery.task(bind=True)
def run_async_task():
    asyncio.run(check_users_for_activity())


async def check_users_for_activity() -> None:
    """Отправляем напоминалку"""
    users = await get_user_for_activity()
    tasks = [asyncio.create_task(
        send_reminder_message(user.get("username")))
        for user in users]
    await asyncio.gather(*tasks)


async def send_reminder_message(chat_id: str) -> None:
    """Отправляем напоминалку"""

    message = 'Ежедневная тренировка памяти 🧠\n' \
              'Пора повторить слова изученные ранее, а может выучить новые'
    await bot.send_message(chat_id=chat_id, text=message)


app_celery.conf.beat_schedule = {
    'check_overdue_tasks': {
        'task': 'tasks.run_async_task',
        'schedule': crontab(hour=14, minute=0)
    },
}

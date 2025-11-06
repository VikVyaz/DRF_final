from celery import shared_task
from .models import UsefulHabit
from decouple import config
import requests
from django.utils import timezone
from datetime import timedelta


TG_TOKEN = config('TG_BOT_KEY')


def send_telegram_message(text, chat_id):
    """def отправки сообщения в бот"""

    params = {
        'text': text,
        'chat_id': chat_id
    }
    url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print('Успешно!')
    else:
        print(f'Не успешно. Ошибка: {response.status_code}')


@shared_task
def send_simple_notification(text, chat_id):
    """Уведомление на create/update/destroy"""

    send_telegram_message(text, chat_id)


@shared_task
def one_hour_notification():
    """Уведомление за час до привычки"""

    habits = UsefulHabit.objects.all()

    now = timezone.now()
    hour = now + timedelta(hours=1)

    upcoming_habits = habits.filter(
        scheduled_time__gt=hour,
        scheduled_time__lt=hour
    )

    if upcoming_habits.exists():
        for habit in upcoming_habits:
            send_telegram_message(
                f'В течении часа нужно сделать привычку {habit.name}',
                habit.owner.telegram_chat_id
            )
    else:
        print('В течении часа привычек не запланировано')

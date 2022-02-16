import os
import redis
from celery import Celery
from celery.schedules import crontab
from .functions import get_env


red = redis.Redis(
    host=get_env('HOST'),
    port=get_env('PORT'),
    password=get_env('PASSWORD')
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletinboard.settings')

app = Celery('bulletinboard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_news_for_week_from_monday': {
        'task': 'board.tasks.send_mail',
        'schedule': crontab(),
    },
}
# 'schedule': crontab(minute=0, hour=8, day_of_week='monday'),


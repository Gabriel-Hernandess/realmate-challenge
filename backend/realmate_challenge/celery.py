from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realmate_challenge.settings')

app = Celery('realmate_challenge')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "generate-daily-summaries": {
        "task": "conversations.tasks.generate_daily_summaries",
        "schedule": crontab(hour=0, minute=0),  # todo dia às 00:00
    },
}
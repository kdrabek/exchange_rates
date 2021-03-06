from __future__ import absolute_import
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_rates.settings")

app = Celery('exchange_rates')

CELERY_TIMEZONE = 'UTC'

app.config_from_object('django.conf:settings')
app.conf.task_routes = {
    'notifications.tasks.*': {'queue': 'notifications'},
    'rates.tasks.*': {'queue': 'rates'},
}
app.conf.beat_schedule = {
    'fetch_rates': {
        'task': 'rates.tasks.find_rates_to_fetch',
        'schedule': 14400.0,
        'args': ()
    },
    'send_notifications': {
        'task': 'notifications.tasks.process_users',
        'schedule': 14400.0,
        'args': ()
    },
}
from __future__ import absolute_import
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_rates.settings")

app = Celery('exchange_rates')

CELERY_TIMEZONE = 'UTC'

app.config_from_object('django.conf:settings')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
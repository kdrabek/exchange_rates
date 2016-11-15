from datetime import datetime, timedelta

from celery import Task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from exchange_rates import app

from rates.downloader.downloader import RatesFetcher
from rates.models import Table


logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_get_current_rates",
    ignore_result=True
)
def fetch_rates():
    fetcher = RatesFetcher()
    next_date = fetcher.find_date_to_fetch()
    if next_date:
        try:
            fetcher.fetch(next_date)
        except Exception as e:
            return fetcher.fetch(next_date + timedelta(days=1))

from datetime import datetime, timedelta

from celery.utils.log import get_task_logger

from exchange_rates import app
from rates.downloader.downloader import RatesFetcher
from rates.models import Table


logger = get_task_logger(__name__)


@app.task
def fetch_rates():
    fetcher = RatesFetcher()
    next_date = fetcher.find_date_to_fetch()
    if not next_date:
        return

    while True:
        try:
            fetcher.fetch(next_date)
        except Exception as e:
            next_date += fetcher.ONE_DAY
        else:
            break

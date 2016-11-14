from datetime import datetime, timedelta

from celery import Task
from celery.utils.log import get_task_logger
from exchange_rates import app

from exchange_rates.rates.downloader.downloader import RatesDownloader
from exchange_rates.rates.models import Table


logger = get_task_logger(__name__)


@app.task
def fetch_rates():
    def _should_run(latest):
        if latest and latest.date >= (datetime.utcnow() - timedelta(days=1)).date():
            return False
        return True

    def _find_latest():
        try:
            return Table.objects.latest('date')
        except Table.DoesNotExist:
            return None

    def _find_next_date(latest):
        if not latest:
            return RatesDownloader.THRESHOLD_DATE
        return latest.date + timedelta(days=1)

    def run(*args, **kwargs):
        latest = _find_latest()
        logger.info("latest: {0}".format(latest))
        logger.info("should run: {0}".format(_should_run(latest)))

        if _should_run(latest):
            next_date = _find_next_date(latest)
            logger.info("next_date: {0}".format(next_date))

            RatesDownloader().download(next_date)

    run()

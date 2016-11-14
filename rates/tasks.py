from datetime import datetime, timedelta

from celery import Task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from exchange_rates import app

from rates.downloader.downloader import RatesDownloader
from rates.models import Table


logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_get_current_rates",
    ignore_result=True
)
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

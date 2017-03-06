from datetime import date, timedelta
from dateutil.parser import parse
from celery.utils.log import get_task_logger

from exchange_rates import app
from rates.models import Table
from rates.downloader.downloader import RatesDownloader, RatesSaver


logger = get_task_logger(__name__)


class RatesFetchingCoordinator(object):

    TABLE = 'A'
    DAYS = 120
    THRESHOLD_DATE = date.today() - timedelta(days=DAYS)

    def get_days_after_threshold(self):
        workdays = []
        day = date.today()
        while day >= self.THRESHOLD_DATE:
            if day.weekday() < 5:
                workdays.append(day)
            day -= timedelta(days=1)
        return set(workdays)

    def get_already_downloaded_dates(self):
        tables = Table.objects.filter(date__gte=self.THRESHOLD_DATE)
        return set([t.date for t in tables])

    def find_dates_to_download(self):
        after_threshold = self.get_days_after_threshold()
        already_downloaded = self.get_already_downloaded_dates()
        return after_threshold - already_downloaded


@app.task
def find_rates_to_fetch():
    coordinator = RatesFetchingCoordinator()
    to_download = list(coordinator.find_dates_to_download())

    for date_to_download in reversed(to_download):
        logger.warning("Publishing with date: %s", date_to_download)
        download_rates.delay(
            date_to_download=date_to_download,
            table=coordinator.TABLE
        )


@app.task(rate_limit="10/m")
def download_rates(date_to_download, table):
    try:
        parsed = parse(date_to_download)
        raw_rates = RatesDownloader().download(parsed.date(), table)
        RatesSaver().save(raw_rates[0])
    except Exception as e:
        logger.error("Exception occurred: %s", str(e))
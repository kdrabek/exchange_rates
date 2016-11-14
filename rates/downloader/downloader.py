import logging
from decimal import Decimal

from datetime import datetime, date
import requests

from rates.models import Currency, Rate, Table
from rates.downloader.exceptions import DateBeforeThreshold, InvalidTableType


log = logging.getLogger(__name__)


class RatesDownloader(object):

    BASE_URL = 'http://api.nbp.pl/api/exchangerates/tables/{table}/{date}'

    def download(self, date, table):
        log.info(
            'Starting fetching rates info for date: {0} table: {1} '.format(
                date, table
            )
        )
        url = self._prepare_url(date, table)
        response = requests.get(url)
        response.raise_for_status()

        return response.json()[0]

    def _prepare_url(self, date, table):
        formatted_date = datetime.strftime(date, "%Y-%m-%d")
        return self.BASE_URL.format(table=table, date=formatted_date)


class RatesSaver(object):

    def save(self, rates_info):
        table = self._create_or_update_table_info(rates_info)
        for rate in rates_info['rates']:
            table_type = rates_info['table']
            currency = self._create_or_update_currency(rate, table_type)
            self._save_rate(rate, currency, table)

    def _create_or_update_table_info(self, rates_info):
        try:
            return Table.objects.get(id=rates_info['no'])
        except Table.DoesNotExist:
            return Table.objects.create(
                id=rates_info['no'],
                type=rates_info['table'],
                date=rates_info['effectiveDate'],
                when_fetched=datetime.utcnow()
            )

    def _save_rate(self, rate, currency, table):
        new_rate = Rate.objects.create(
            currency=currency,
            table=table,
            rate=Decimal(rate['mid'])
        )

    def _create_or_update_currency(self, rate, table_type):
        try:
            return Currency.objects.get(code=rate['code'])
        except Currency.DoesNotExist:
            return Currency.objects.create(
                code=rate['code'],
                name=rate.get('currency') or rate.get('country'),
                table_type=table_type
            )


class RatesFetcher(object):

    DEFAULT_TABLE = 'A'
    ALLOWED_TABLES = ['A', 'B', 'C']
    THRESHOLD_DATE = date(2002, 1, 2)

    def __init__(self):
        self._downloader = RatesDownloader()
        self._saver = RatesSaver()

    def fetch(self, date, table=DEFAULT_TABLE):
        self.validate(date, table)
        try:
            raw_data = self._downloader.download(date, table)
        except Exception:
            pass
        else:
            for rates_information in raw_data:
                self._saver.save(rates_information)

    def validate(self, date, table):
        if date < self.THRESHOLD_DATE:
            raise DateBeforeThreshold()
        if table not in self.ALLOWED_TABLES:
            raise InvalidTableType()

    def _should_run(self, latest):
        if latest and latest.date >= (datetime.utcnow() - timedelta(days=1)).date():
            return False
        return True

    def _find_latest(self,):
        try:
            return Table.objects.latest('date')
        except Table.DoesNotExist:
            return None

    def _find_next_date(self, latest):
        if not latest:
            return RatesDownloader.THRESHOLD_DATE
        return latest.date + timedelta(days=1)

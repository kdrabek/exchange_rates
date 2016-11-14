import logging
from decimal import Decimal

from datetime import datetime, date
import requests

from exchange_rates.rates.models import Currency, Rate, Table


log = logging.getLogger(__name__)


class DateBeforeThreshold(Exception):
    pass


class TableNameInvalid(Exception):
    pass


class RatesFetcher(object):

    BASE_URL = 'http://api.nbp.pl/api/exchangerates/tables/{table}/{date}'

    def fetch(self, date, table):
        log.info(
            'Starting fetching rates info for date: {0} table: {1} '.format(
                date, table
            )
        )
        url = self._prepare_url(date, table)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HttpError as e:
            log.error('{0} occurred for date: {1} table: {2} '.format(
                    e, date, table
                )
            )
            raise
        else:
            return response.json()[0]

    def _prepare_url(self, date, table):
        formatted_date = datetime.strftime(date, "%Y-%m-%d")
        return self.BASE_URL.format(table=table, date=formatted_date)


class RatesSaver(object):

    def save(self, raw_data):
        table = self._save_table(raw_data)
        for rate in raw_data['rates']:
            table_type = raw_data['table']
            currency = self._save_currency(rate, table_type)
            self._save_rate(rate, currency, table)

    def _save_table(self, raw_data):
        try:
            return Table.objects.get(id=raw_data['no'])
        except Table.DoesNotExist:
            return Table.objects.create(
                id=raw_data['no'],
                type=raw_data['table'],
                date=raw_data['effectiveDate'],
                when_fetched=datetime.utcnow()
            )

    def _save_rate(self, rate, currency, table):
        new_rate = Rate.objects.create(
            currency=currency,
            table=table,
            rate=Decimal(rate['mid'])
        )

    def _save_currency(self, rate, table_type):
        try:
            return Currency.objects.get(code=rate['code'])
        except Currency.DoesNotExist:
            return Currency.objects.create(
            code=rate['code'],
            name=rate.get('currency') or rate.get('country'),
            table_type=table_type
            )


class RatesDownloader(object):

    DEFAULT_TABLE = 'A'
    ALLOWED_TABLES = ['A', 'B', 'C']
    THRESHOLD_DATE = date(2002, 1, 2)

    def __init__(self):
        self._fetcher = RatesFetcher()
        self._saver = RatesSaver()

    def _validate(self, date, table):
        if date < self.THRESHOLD_DATE:
            raise DateBeforeThreshold()
        if table not in self.ALLOWED_TABLES:
            raise TableNameInvalid()
        return True

    def download(self, date, table=DEFAULT_TABLE):
        if self._validate(date, table):
            raw_data = self._fetcher.fetch(date, table)
            self._saver.save(raw_data)

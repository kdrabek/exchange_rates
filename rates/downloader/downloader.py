from datetime import datetime
from decimal import Decimal
import logging

import requests

from rates.models import Currency, Rate, Table


log = logging.getLogger(__name__)


class RatesDownloader(object):

    BASE_URL = 'http://api.nbp.pl/api/exchangerates/tables/{table}/{date}'
    ALLOWED_TABLES = ['A', 'B', 'C']

    def __init__(self, threshold_date):
        self.saver = RatesSaver()
        self.threshold_date = threshold_date

    def download(self, date, table):
        if not self._is_valid_request(date, table):
            return

        log.info('Downloading for date: {0} table: {1} '.format(date, table))
        url = self._prepare_url(date, table)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _prepare_url(self, date, table):
        formatted_date = datetime.strftime(date, "%Y-%m-%d")
        return self.BASE_URL.format(table=table, date=formatted_date)

    def _is_valid_request(self, date, table):
        if not self.threshold_date <= date <= date.today():
            return False

        return table in self.ALLOWED_TABLES


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
        Rate.objects.create(
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

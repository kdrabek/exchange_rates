from datetime import date, timedelta
import os

import pytest
from mock import patch, MagicMock, sentinel
from vcr import use_cassette

from rates.downloader.downloader import (
    RatesFetcher, RatesSaver, RatesDownloader,
)
from rates.models import Table, Rate, Currency


HERE = os.path.dirname(os.path.realpath(__file__))


class TestRatesDownloader(object):

    @pytest.fixture
    def downloader(self):
        return RatesDownloader()

    def assert_rate_dict_is_correct(self, rates_dict):
        single_rate_dict = rates_dict['rates'][0]
        assert isinstance(rates_dict, dict)
        assert isinstance(rates_dict['rates'], list)
        assert 'effectiveDate' in rates_dict
        assert 'table' in rates_dict
        assert 'no' in rates_dict
        assert sorted(single_rate_dict.keys()) == sorted(
            ['code', 'currency', 'mid']
        )

    @use_cassette(os.path.join(HERE, 'cassettes/tableA.yml'))
    def test_fetch(self, downloader):
        response = downloader.download(date=date(2016, 11, 7), table='A')
        rates_dict = response[0]

        assert isinstance(response, list)
        self.assert_rate_dict_is_correct(rates_dict)


    @patch('rates.downloader.downloader.requests')
    def test_fetch_get_uses_correct_url(self, mock_requests, downloader):
        downloader.download(date=date(2016, 11, 7), table='A')
        expected_url = downloader.BASE_URL.format(table='A', date='2016-11-07')

        mock_requests.get.assert_called_once_with(expected_url)


@pytest.mark.django_db
class TestRatesSaver(object):

    @pytest.fixture
    def saver(self):
        return RatesSaver()

    @pytest.fixture
    def raw_data(self):
        return {
            'effectiveDate': '2016-11-07',
            'table': 'A',
            'no': '111/A/NBP/YYYY',
            'rates': [{
                'code': 'XXX',
                'currency': 'test_currency',
                'mid': '11.2345'
            }]
        }

    def test_save(self, saver, raw_data):
        assert len(Table.objects.all()) == 0
        assert len(Rate.objects.all()) == 0
        assert len(Currency.objects.all()) == 0

        saver.save(raw_data)

        assert len(Rate.objects.all()) == 1
        assert len(Table.objects.all()) == 1
        assert len(Currency.objects.all()) == 1


@pytest.mark.django_db
class TestRatesFetcher(object):

    @pytest.fixture
    def downloader_return_value(self):
        return [sentinel]

    @pytest.fixture
    def fetcher(self, downloader_return_value):
        fetcher = RatesFetcher()
        fetcher.downloader = MagicMock(spec=RatesDownloader)
        fetcher.downloader.download.return_value = downloader_return_value
        fetcher.saver = MagicMock(spec=RatesSaver)
        return fetcher

    @pytest.mark.parametrize('date, table', [
        (date(2015, 5, 30), 'A'), (date(2016, 11, 10), 'B'),
        (date(2016, 4, 10), 'C')
    ])
    def test_fetch_uses_downloader_and_saver(
        self, fetcher, date, table, downloader_return_value):
        fetcher.fetch(date=date, table=table)

        fetcher.downloader.download.assert_called_once_with(date, table)
        fetcher.saver.save.assert_called_once_with(downloader_return_value[0])

    def test_fetch_raises_error_date_before_threshold(self, fetcher):
        fetcher.fetch(date(1999, 12, 31), table='A')

        assert not fetcher.downloader.download.called
        assert not fetcher.saver.save.called

    def test_download_raises_error_incorrect_table(self, fetcher):
        fetcher.fetch(date(2015, 12, 31), table='Z')

        assert not fetcher.downloader.download.called
        assert not fetcher.saver.save.called

    def test_find_date_to_fetch_no_last_entry(self, fetcher):
        to_fetch = fetcher.find_date_to_fetch()

        assert to_fetch == fetcher.THRESHOLD_DATE

    def test_find_date_to_fetch_last_entry_exist(
        self, fetcher, saved_test_table):
        to_fetch = fetcher.find_date_to_fetch()

        assert to_fetch == saved_test_table.date + timedelta(days=1)

    def test_find_date_to_fetch_last_entry_friday(
        self, fetcher, saved_test_table):
        saved_test_table.date = date(2016, 11, 4)
        saved_test_table.save()
        to_fetch = fetcher.find_date_to_fetch()

        assert to_fetch == saved_test_table.date + timedelta(days=3)

    def test_find_date_to_fetch_last_entry_younger_than_a_day(
        self, fetcher, saved_test_table):
        saved_test_table.date = date.today()
        saved_test_table.save()
        to_fetch = fetcher.find_date_to_fetch()

        assert to_fetch is None

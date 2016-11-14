import os
from datetime import date

import pytest
from mock import patch, MagicMock, sentinel
from vcr import use_cassette

from rates.downloader.downloader import (
    RatesFetcher, RatesSaver, RatesDownloader,
    DateBeforeThreshold, TableNameInvalid
)
from rates.models import Table, Rate, Currency


HERE = os.path.dirname(os.path.realpath(__file__))


class TestRatesFetcher(object):

    @pytest.fixture
    def fetcher(self):
        return RatesFetcher()

    @use_cassette(os.path.join(HERE, 'cassettes/tableA.yml'))
    def test_fetch(self, fetcher):
        response = fetcher.fetch(date=date(2016, 11, 7), table='A')
        sample_rate = response['rates'][0]

        assert isinstance(response, dict)
        assert isinstance(response['rates'], list)
        assert 'effectiveDate' in response
        assert 'table' in response
        assert 'no' in response
        assert sorted(sample_rate.keys()) == sorted(
            ['code', 'currency', 'mid']
        )

    @patch('rates.downloader.downloader.requests')
    def test_fetch_get_uses_correct_url(self, mock_requests, fetcher):
        fetcher.fetch(date=date(2016, 11, 7), table='A')
        expected_url = fetcher.BASE_URL.format(table='A', date='2016-11-07')

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


class TestRatesDownloader(object):

    @pytest.fixture
    def fetcher_return_value(self):
        return sentinel

    @pytest.fixture
    def downloader(self, fetcher_return_value):
        downloader = RatesDownloader()
        downloader._fetcher = MagicMock(spec=RatesFetcher)
        downloader._fetcher.fetch.return_value = fetcher_return_value
        downloader._saver = MagicMock(spec=RatesSaver)
        return downloader

    @pytest.mark.parametrize('date, table', [
        (date(2015, 5, 30), 'A'), (date(2016, 11, 10), 'B'),
        (date(2016, 4, 10), 'C')
    ])
    def test_download_uses_fetcher_and_saver(
        self, downloader, date, table, fetcher_return_value):
        downloader.download(date=date, table=table)

        downloader._fetcher.fetch.assert_called_once_with(date, table)
        downloader._saver.save.assert_called_once_with(fetcher_return_value)

    def test_download_raises_error_date_before_threshold(self, downloader):
        with pytest.raises(DateBeforeThreshold):
            downloader.download(date(1999, 12, 31), table='A')

    def test_download_raises_error_incorrect_table(self, downloader):
        with pytest.raises(TableNameInvalid):
            downloader.download(date(2015, 12, 31), table='Z')

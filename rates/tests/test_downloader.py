import os
from datetime import date

import pytest
from mock import patch, MagicMock, sentinel
from vcr import use_cassette

from rates.downloader.downloader import (
    RatesFetcher, RatesSaver, RatesDownloader,
    DateBeforeThreshold, InvalidTableType
)
from rates.models import Table, Rate, Currency


HERE = os.path.dirname(os.path.realpath(__file__))


class TestRatesDownloader(object):

    @pytest.fixture
    def downloader(self):
        return RatesDownloader()

    @use_cassette(os.path.join(HERE, 'cassettes/tableA.yml'))
    def test_fetch(self, downloader):
        response = downloader.download(date=date(2016, 11, 7), table='A')
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


class TestRatesFetcher(object):

    @pytest.fixture
    def fetcher_return_value(self):
        return [sentinel]

    @pytest.fixture
    def fetcher(self, fetcher_return_value):
        fetcher = RatesFetcher()
        fetcher._downloader = MagicMock(spec=RatesDownloader)
        fetcher._downloader.download.return_value = fetcher_return_value
        fetcher._saver = MagicMock(spec=RatesSaver)
        return fetcher

    @pytest.mark.parametrize('date, table', [
        (date(2015, 5, 30), 'A'), (date(2016, 11, 10), 'B'),
        (date(2016, 4, 10), 'C')
    ])
    def test_fetch_uses_downloader_and_saver(
        self, fetcher, date, table, fetcher_return_value):
        fetcher.fetch(date=date, table=table)

        fetcher._downloader.download.assert_called_once_with(date, table)
        fetcher._saver.save.assert_called_once_with(fetcher_return_value[0])

    def test_fetch_raises_error_date_before_threshold(self, fetcher):
        with pytest.raises(DateBeforeThreshold):
            fetcher.fetch(date(1999, 12, 31), table='A')

    def test_download_raises_error_incorrect_table(self, fetcher):
        with pytest.raises(InvalidTableType):
            fetcher.fetch(date(2015, 12, 31), table='Z')

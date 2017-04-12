import os
from datetime import date, datetime, timedelta

import freezegun
import mock
import pytest
from vcr import use_cassette

from rates.downloader.downloader import RatesDownloader, RatesSaver
from rates.models import Currency, Rate, Table

HERE = os.path.dirname(os.path.realpath(__file__))


@freezegun.freeze_time('2017-02-10 20:00:00')
class TestRatesDownloader(object):

    @pytest.fixture
    @freezegun.freeze_time('2017-02-10 20:00:00')
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
    @freezegun.freeze_time('2016-11-07 20:00:00')  # changing will change vcr
    def test_download(self, downloader):
        response = downloader.download(date=date.today(), table='A')
        rates_dict = response[0]

        assert isinstance(response, list)
        self.assert_rate_dict_is_correct(rates_dict)

    @mock.patch('rates.downloader.downloader.requests')
    def test_fetch_get_uses_correct_url(self, mock_requests, downloader):
        downloader.download(date=date.today(), table='A')
        formatted = datetime.strftime(date.today(), "%Y-%m-%d")
        expected_url = downloader.BASE_URL.format(table='A', date=formatted)

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
        assert Table.objects.count() == 0
        assert Rate.objects.count() == 0
        assert Currency.objects.count() == 0

        saver.save(raw_data)

        assert Rate.objects.count() == 1
        assert Table.objects.count() == 1
        assert Currency.objects.count() == 1

from datetime import date, datetime, timedelta

import freezegun
import mock
import pytest

from rates.downloader.downloader import RatesDownloader, RatesSaver
from rates.models import Table
from rates.tasks import (
    find_rates_to_fetch, download_rates, RatesFetchingCoordinator
)


@pytest.fixture
def raw_downloaded_data():
    return [{
        'effectiveDate': '2016-11-07',
        'table': 'A',
        'no': '111/A/NBP/YYYY',
        'rates': [{
            'code': 'XXX',
            'currency': 'test_currency',
            'mid': '11.2345'
        }]
    }]


@mock.patch.object(RatesFetchingCoordinator, 'find_dates_to_download')
@mock.patch('rates.tasks.download_rates')
def test_find_rates_to_fetch(mock_download_rates, mock_find_rates):
    test_date = date.today()
    mock_find_rates.return_value = [test_date]

    find_rates_to_fetch()

    mock_download_rates.delay.assert_called_once_with(
        date_to_download=test_date, table='A'
    )


@mock.patch.object(RatesDownloader, 'download')
@mock.patch.object(RatesSaver, 'save')
def test_download_rates(mock_save, mock_download, raw_downloaded_data):
    mock_download.return_value = raw_downloaded_data

    download_rates(str(date.today()), 'A')

    mock_download.assert_called_once_with(date.today(), 'A')
    mock_save.assert_called_once_with(raw_downloaded_data[0])


@mock.patch.object(RatesDownloader, 'download')
@mock.patch.object(RatesSaver, 'save')
@mock.patch('rates.tasks.logger')
def test_download_rates_when_exception_is_raised(
        mock_logger, mock_save, mock_download, raw_downloaded_data):
    test_exception = Exception("Some error occurred")
    mock_download.side_effect = test_exception

    download_rates(str(date.today()), 'A')

    mock_logger.error.assert_called_once_with(
        'Exception occurred: %s', str(test_exception)
    )


@freezegun.freeze_time('2017-02-10 20:00:00')
@pytest.mark.django_db
class TestRatesFetchingCoordinator(object):

    @pytest.fixture
    def coordinator(self):
        return RatesFetchingCoordinator()

    @pytest.fixture
    def table(db):
        return Table.objects.create(
            id='1/A/3456', type='A', date=date.today(),
            when_fetched=datetime.utcnow()
        )

    def test_get_days_after_threshold(self, coordinator):
        coordinator.THRESHOLD_DATE = date.today() - timedelta(days=1)
        days_after_threshold = list(coordinator.get_days_after_threshold())
        expected = [date.today()-timedelta(days=1), date.today()]

        assert sorted(days_after_threshold) == sorted(expected)

    def test_get_already_downloaded_dates(self, coordinator, table):
        downloaded = coordinator.get_already_downloaded_dates()

        assert list(downloaded) == [table.date]

    def test_find_dates_to_download(self, coordinator, table):
        coordinator.THRESHOLD_DATE = date.today() - timedelta(days=1)
        to_download = coordinator.find_dates_to_download()

        assert table.date not in to_download
        assert list(to_download) == [date.today()-timedelta(days=1)]

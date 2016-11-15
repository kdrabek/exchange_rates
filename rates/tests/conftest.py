from datetime import datetime, date, timezone

from freezegun import freeze_time
import pytest

from rates.models import Table


@pytest.fixture
def test_currency():
    return {
        'code': 'GBP',
        'name': 'British Pounds',
        'table_type': 'A'
    }


@pytest.fixture
@freeze_time("2016-11-09 10:00:00")
def test_table():
    return {
        'id': 'SOME/TABLE/ID',
        'type': 'A',
        'date': date.today(),
        'when_fetched': datetime.now(timezone.utc)
    }


@pytest.fixture
def saved_test_table(test_table):
    return Table.objects.create(**test_table)

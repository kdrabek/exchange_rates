from decimal import Decimal

import pytest
from freezegun import freeze_time

from rates.models import Currency, Rate, Table
from rates.utils import CODE_TO_COUNTRY


@pytest.fixture
def currency(db, test_currency):
    return Currency.objects.create(**test_currency)


@pytest.fixture
def table(db, test_table):
    return Table.objects.create(**test_table)


@pytest.fixture
def rate_value(db):
    return Decimal('12.3456')


def test_creates_valid_currency_model(db, test_currency):
    currency = Currency.objects.create(**test_currency)

    assert isinstance(currency, Currency)
    assert currency.code == test_currency['code']
    assert currency.name == test_currency['name']
    assert currency.table_type == test_currency['table_type']
    assert currency.country == CODE_TO_COUNTRY.get(test_currency['code'])


@freeze_time("2016-11-09 10:00:00")
def test_creates_valid_table_model(db, test_table):
    table = Table.objects.create(**test_table)

    assert isinstance(table, Table)
    assert table.id == test_table['id']
    assert table.type == test_table['type']
    assert table.date == test_table['date']
    assert table.when_fetched == test_table['when_fetched']


@freeze_time("2016-11-09 10:00:00")
def test_creates_valid_rate_model(db, currency, table, rate_value):
    rate = Rate.objects.create(
        currency=currency, rate=rate_value, table=table)

    assert isinstance(rate, Rate)
    assert rate.currency == currency
    assert rate.table == table
    assert rate.rate == rate_value
    assert rate.relative_change == Decimal('0.00')

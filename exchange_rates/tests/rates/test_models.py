from decimal import Decimal

from freezegun import freeze_time
import pytest

from rates.models import Currency, Rate, Table


@pytest.mark.django_db
class TestCurrency(object):

    def test_creates_valid_model(self, test_currency):
        currency = Currency.objects.create(**test_currency)

        assert isinstance(currency, Currency)
        assert currency.code == test_currency['code']
        assert currency.name == test_currency['name']
        assert currency.table_type == test_currency['table_type']


@pytest.mark.django_db
@freeze_time("2016-11-12 10:00:00")
class TestTable(object):

    def test_creates_valid_model(self, test_table):
        table = Table.objects.create(**test_table)

        assert isinstance(table, Table)
        assert table.id == test_table['id']
        assert table.type == test_table['type']
        assert table.date == test_table['date']
        assert table.when_fetched == test_table['when_fetched']


@pytest.mark.django_db
@freeze_time("2016-11-12 10:00:00")
class TestRate(object):

    @pytest.fixture
    def currency(self, test_currency):
        currency = Currency.objects.create(**test_currency)
        return currency

    @pytest.fixture
    def table(self, test_table):
        table = Table.objects.create(**test_table)
        return table

    @pytest.fixture
    def rate_value(self):
        return Decimal('12.3456')

    def test_creates_valid_model(self, currency, table, rate_value):
        rate = Rate.objects.create(
            currency=currency, rate=rate_value, table=table)

        assert isinstance(rate, Rate)
        assert rate.currency == currency
        assert rate.table == table
        assert rate.rate == rate_value

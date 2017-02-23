from decimal import Decimal
from datetime import datetime, date
import pytest

from rates.models import Currency, Rate, Table
from rates.serializers import (
    CurrencySerializer, RatesSerializer, RateDetailsSerializer
)


@pytest.fixture
def currency(db):
    return Currency(code='ABC', name='Test Currency', table_type='A')


@pytest.fixture
def table(db):
    return Table(
        id='1/A/3456', type='A', date=date.today(),
        when_fetched=datetime.utcnow()
    )


class TestCurrencySerializer(object):

    @pytest.fixture
    def serializer(self):
        return CurrencySerializer

    def test_currency_object_is_serialized(self, serializer, currency):
        assert serializer(currency).data == {
            'code': 'ABC', 'name': 'Test Currency', 'table_type': 'A'
        }

    def test_currency_objects_with_missing_attribute(self, serializer):
        currency = Currency(code='ABC', name='Test Currency')

        assert serializer(currency).data == {
            'code': 'ABC', 'name': 'Test Currency', 'table_type': ''
        }


class TestRatesSerializer(object):

    @pytest.fixture
    def serializer(self):
        return RatesSerializer

    def test_rate_object_is_serialized(self, serializer, currency):
        rate = Rate(currency=currency, rate=Decimal('12.34'))

        assert serializer(rate).data == {
            'currency': 'ABC', 'rate': '12.3400', 'name': 'Test Currency'
        }


@pytest.mark.django_db
class TestRateDetailsSerializer(object):

    @pytest.fixture
    def serializer(self):
        return RateDetailsSerializer

    def test_rate_object_is_serialized(self, serializer, currency, table):
        rate = Rate(currency=currency, rate=Decimal('12.34'), table=table)
        rate.save()

        assert serializer(rate).data == {
            'currency': currency.code,
            'rate': '{0:.4f}'.format(rate.rate),
            'name': currency.name,
            'date': table.date,
            'relative_change': '0.0000'
        }

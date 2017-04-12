from datetime import date, datetime
from decimal import Decimal

import pytest

from rates.models import Currency, Rate, Table
from rates.serializers import (
    CurrencySerializer, RateDetailsSerializer, RatesSerializer
)
from rates.utils import CODE_TO_COUNTRY


@pytest.fixture
def currency(db):
    return Currency(code='GBP', name='Test Currency', table_type='A')


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
            'code': 'GBP', 'name': 'Test Currency', 'table_type': 'A',
            'country': CODE_TO_COUNTRY.get(currency.code)
        }

    def test_currency_objects_with_missing_attribute(self, serializer):
        currency = Currency(code='GBP', name='Test Currency')

        assert serializer(currency).data == {
            'code': 'GBP', 'name': 'Test Currency', 'table_type': '',
            'country': CODE_TO_COUNTRY.get(currency.code)
        }


class TestRatesSerializer(object):

    @pytest.fixture
    def serializer(self):
        return RatesSerializer

    def test_rate_object_is_serialized(self, serializer, currency):
        rate = Rate(currency=currency, rate=Decimal('12.34'))

        assert serializer(rate).data == {
            'currency': 'GBP', 'rate': '12.3400', 'name': 'Test Currency',
            'country': CODE_TO_COUNTRY[currency.code]
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
            'relative_change': '0.0000',
            'country': CODE_TO_COUNTRY[currency.code]
        }

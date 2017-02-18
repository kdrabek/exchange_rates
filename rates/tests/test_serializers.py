from decimal import Decimal

import pytest

from rates.models import Currency, Rate
from rates.serializers import CurrencySerializer, RatesSerializer


@pytest.fixture
def currency():
    return Currency(code='ABC', name='Test Currency', table_type='A')

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
            'currency': 'ABC', 'rate': '12.34', 'name': 'Test Currency'
        }

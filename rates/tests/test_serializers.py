import pytest

from rates.models import Currency
from rates.serializers import CurrencySerializer


class TestCurrencySerializer:

    @pytest.fixture
    def serializer(self):
        return CurrencySerializer

    def test_currency_object_is_serialized(self, serializer):
        currency = Currency(code='ABC', name='Test Currency', table_type='A')

        assert serializer(currency).data == {
            'code': 'ABC', 'name': 'Test Currency', 'table_type': 'A'
        }

    def test_currency_objects_with_missing_attribute(self, serializer):
        currency = Currency(code='ABC', name='Test Currency')

        assert serializer(currency).data == {
            'code': 'ABC', 'name': 'Test Currency', 'table_type': ''
        }

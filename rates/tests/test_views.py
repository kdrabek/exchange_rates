import json
import pytest

from django.core.urlresolvers import reverse
from rest_framework.status import HTTP_200_OK

from rates.models import Currency


@pytest.mark.django_db
class TestLoginView(object):

    @pytest.fixture
    def saved_currencies(self):
        Currency(code='ABC', name='Currency', table_type='A').save()
        Currency(code='ZXY', name='Other Currency', table_type='A').save()

    def assert_response(self, response, expected_len, expected_keys):
        data = json.loads(response.json())
        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == expected_len

        if expected_len > 0:
            assert isinstance(data[0], dict)
            assert sorted(expected_keys) == sorted(data[0].keys())

    def test_get_all_currency_info(self, client, saved_currencies):
        response = client.get(reverse('rates:currency'))

        self.assert_response(
            response, expected_len=2,
            expected_keys=['code', 'name', 'table_type']
        )

    @pytest.mark.parametrize('code, results_count', [('ABC', 1), ('CDE', 0)])
    def test_get_with_currency_filter(
            self, client, saved_currencies, code, results_count):
        response = client.get(reverse('rates:currency'), {'code': code})

        self.assert_response(
            response, expected_len=results_count,
            expected_keys=['code', 'name', 'table_type']
        )

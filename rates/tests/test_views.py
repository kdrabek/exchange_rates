from decimal import Decimal
from datetime import date, datetime, timedelta
import pytest

from django.core.urlresolvers import reverse
from rest_framework.status import (
    HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
)

from rates.models import Currency, Rate, Table
from authentication.models import User


class Fixtures(object):

    @pytest.fixture
    def saved_currencies(self):
        Currency(code='ABC', name='Currency', table_type='A').save()
        Currency(code='ZXY', name='Other Currency', table_type='A').save()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email='test@email.com', password='password'
        )

    @pytest.fixture
    def token(self, user):
        return user.auth_token.key

    @pytest.fixture
    def saved_currency(self):
        currency = Currency(code='ABC', name='Currency', table_type='A')
        currency.save()
        return currency

    @pytest.fixture
    def saved_table(self):
        table = Table(
            id='some-id', type='A', date=date.today(),
            when_fetched=datetime.utcnow())
        table.save()
        return table

    @pytest.fixture
    def saved_rate(self, saved_currency, saved_table):
        rate = Rate(
            rate=Decimal('12.34'), table=saved_table, currency=saved_currency)
        rate.save()
        return rate


@pytest.mark.django_db
class TestCurrencyView(Fixtures):

    def assert_response(self, response, expected_len, expected_keys):
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == expected_len

        if expected_len > 0:
            assert isinstance(data[0], dict)
            assert sorted(expected_keys) == sorted(data[0].keys())

    def test_unauthenticated_user_is_unauthorized(self, client):
        response = client.get(reverse('rates:currency'))

        assert  response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_all_currency_info(self, client, saved_currencies, token):
        response = client.get(
            reverse('rates:currency'),
            HTTP_AUTHORIZATION='Token {}'.format(token)
        )

        self.assert_response(
            response, expected_len=2,
            expected_keys=['code', 'name', 'table_type']
        )

    @pytest.mark.parametrize('code, results_count', [('ABC', 1), ('CDE', 0)])
    def test_get_with_currency_filter(
            self, client, token, saved_currencies, code, results_count):
        response = client.get(
            reverse('rates:currency'),
            {'code': code},
            HTTP_AUTHORIZATION='Token {}'.format(token)
        )

        self.assert_response(
            response, expected_len=results_count,
            expected_keys=['code', 'name', 'table_type']
        )


@pytest.mark.django_db
class TestRatesView(Fixtures):

    @pytest.fixture
    def today(self):
        today = datetime.today()
        return datetime.strftime(today, '%Y-%m-%d')

    @pytest.fixture
    def tomorrow(self):
        today = datetime.today() + timedelta(days=1)
        return datetime.strftime(today, '%Y-%m-%d')

    def assert_response(self, response, expected_date):
        json = response.json()
        assert response.status_code == HTTP_200_OK
        assert json['table_date'] == expected_date
        assert json['rates'][0] == {
            'currency':'ABC',
            'name':'Currency',
            'rate':'12.3400'
        }

    def test_get_latest_rates(self, client, saved_rate, today):
        response = client.get(
            reverse('rates:rates_latest'),
        )
        self.assert_response(response, today)

    def test_get_rates_for_given_date(self, client, saved_rate, today):
        response = client.get(
            reverse('rates:rates_for_date', kwargs={'date': today})
        )
        self.assert_response(response, today)

    def test_get_rates_for_given_date_returns_date_closest_date(
            self, client, saved_rate, tomorrow, today):
        response = client.get(
            reverse('rates:rates_for_date', kwargs={'date': tomorrow}),
        )
        # because we don't have future rates, today's are fetched
        self.assert_response(response, expected_date=today)


@pytest.mark.django_db
class TestRatesDetailsView(Fixtures):

    def test_unauthenticated_user_is_unauthorized(self, client):
        response = client.get(
            reverse(
                'rates:rate_detail_view',
                kwargs={'currency_code': 'AUD', 'limit': 5}
            )
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_rates_details(self, client, saved_rate, user, token):
        limit = 1
        response = client.get(
            reverse(
                'rates:rate_detail_view',
                kwargs={
                    'currency_code':  saved_rate.currency.code,
                    'limit': limit
                }
            ),
            HTTP_AUTHORIZATION='Token {}'.format(token)
        )

        json = response.json()

        assert response.status_code == HTTP_200_OK
        assert len(json['rates']) == limit
        assert json['rates'][0] == {
            'currency': saved_rate.currency.code,
            'date': str(saved_rate.table.date),
            'name': saved_rate.currency.name,
            'rate': '{0:.4f}'.format(saved_rate.rate),
            'relative_change': '0.0000'
        }

    def test_get_rates_details_404_for_non_existing_currency_code(
            self, client, saved_rate, user, token):
        limit = 1
        response = client.get(
            reverse(
                'rates:rate_detail_view',
                kwargs={
                    'currency_code': 'XYZ',
                    'limit': limit
                }
            ),
            HTTP_AUTHORIZATION='Token {}'.format(token)
        )

        assert response.status_code == HTTP_404_NOT_FOUND

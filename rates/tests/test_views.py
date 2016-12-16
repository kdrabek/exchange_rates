import pytest

from django.core.urlresolvers import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from rates.models import Currency
from authentication.models import User


@pytest.mark.django_db
class TestLoginView(object):

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

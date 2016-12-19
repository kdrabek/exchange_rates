import pytest

from django.core.urlresolvers import reverse
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
)

from rates.models import Currency
from notifications.models import Notification
from authentication.models import User


@pytest.mark.django_db
class TestNotificationsListView(object):

    @pytest.fixture
    def token(self, user):
        return user.auth_token.key

    @pytest.fixture
    def post_data(self):
        return {'code': 'AUD', 'rate': '23.45', "threshold": "ABOVE"}


    def assert_response(self, response, expected_len, expected_keys):
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == expected_len

        if expected_len > 0:
            assert isinstance(data[0], dict)
            assert sorted(expected_keys) == sorted(data[0].keys())

    def test_unauthenticated_user_is_unauthorized(self, client, user):
        response = client.get(
            reverse('notifications:list', kwargs={'user_id': user.id})
        )

        assert  response.status_code == HTTP_401_UNAUTHORIZED

    def test_authenticated_user_cannot_access_another_users_resource(
            self, client, user, token):
        response = client.get(
            reverse('notifications:list', kwargs={'user_id': user.id + 1}),
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert  response.status_code == HTTP_403_FORBIDDEN

    def test_authenticated_user_can_get_nofification_list(
            self, client, user, token, notification):
        response = client.get(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        self.assert_response(
            response, expected_len=1,
            expected_keys=['currency', 'rate', 'threshold', 'user']
        )

    def test_authenticated_user_can_create_new_notification(
            self, client, user, token, currency, post_data):
        response = client.post(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            post_data, HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert response.status_code == HTTP_200_OK
        assert Notification.objects.filter(user=user).count() == 1

    def test_404_raised_when_invalid_currency(
            self, client, user, token, currency, post_data):
        post_data['code'] = 'XXX'
        response = client.post(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            post_data, HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert response.status_code == HTTP_404_NOT_FOUND
        assert Notification.objects.filter(user=user).count() == 0

    def test_bad_request_raised_when_invalid_post_data(
            self, client, user, token, currency, post_data):
        post_data['rate'] = '1.23456'  # to many decimal places
        response = client.post(
            reverse('notifications:list', kwargs={'user_id': user.id}),
            post_data, HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert Notification.objects.filter(user=user).count() == 0

import pytest

from django.core.urlresolvers import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class TestLoginView(object):

    def test_post_when_credentials_not_present(self, client):
        response = client.post(reverse('auth:login'), {})

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'error': 'Password or email is missing'}

    def test_post_with_incorrect_credentials(self, client, user):
        response = client.post(
            reverse('auth:login'),
            {'email': user.email, 'password': 'incorrect-password'}
        )

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'error': 'Could not authenticate using provided credentials'
        }

    def test_post_with_correct_credentials(self, client, user):
        response = client.post(
            reverse('auth:login'),
            {'email': user.email, 'password': 'password'}
        )

        assert response.status_code == HTTP_200_OK
        assert response.data['token'] is not None


@pytest.mark.django_db
class TestRegisterView(object):

    def test_post_when_credentials_not_present(self, client):
        response = client.post(reverse('auth:register'), {})

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'error': 'Password or email is missing'}

    def test_post_when_user_already_exists(self, client, user):
        response = client.post(
            reverse('auth:register'),
            {'email': user.email, 'password': 'incorrect-password'}
        )

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            'error': 'User already exists.'
        }

    def test_post_with_correct_credentials(self, client):
        response = client.post(
            reverse('auth:register'),
            {'email': 'some@email.com', 'password': 'password'}
        )

        assert response.status_code == HTTP_200_OK
        assert response.data['token'] is not None

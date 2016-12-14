import pytest

from rest_framework.test import APIClient

from authentication.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@email.com', password='password'
    )

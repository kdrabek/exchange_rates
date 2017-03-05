from decimal import Decimal
from datetime import date, datetime

import pytest

from authentication.models import User
from rates.models import Currency, Rate, Table
from notifications.models import Notification


@pytest.fixture
def user(db):
    return User.objects.create(email='test@email.com', password='password')


@pytest.fixture
def another_user():
    return User.objects.create(
        email='another_test@email.com', password='password')


@pytest.fixture
def currency(db):
    return Currency.objects.create(
        code='AUD', name='Australian Dollar', table_type='A')


@pytest.fixture
def notification(db, user, currency):
    return Notification.objects.create(
            user=user, currency=currency, rate='12.34', threshold='ABOVE'
        )


@pytest.fixture
def table(db):
    return Table.objects.create(
        id='1/A/2016', type='A', date=date.today(),
        when_fetched=datetime.utcnow()
    )


@pytest.fixture
def rate(db, currency, table):
    return Rate.objects.create(
        currency=currency, rate=Decimal('1.23'), table=table)


@pytest.fixture
def token(user):
    return user.auth_token.key

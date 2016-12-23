from decimal import Decimal

import pytest

from notifications.serializers import NotificationSerializer


@pytest.mark.django_db
class TestCurrencySerializer:

    @pytest.fixture
    def serializer(self):
        return NotificationSerializer

    def test_notification_object_is_serialized(self, serializer, notification):
        assert serializer(notification).data == {
            'user': notification.user.id,
            'id': notification.id,
            'currency': notification.currency.code,
            'rate': notification.rate,
            'threshold': notification.threshold,
        }

    def test_notification_object_is_created(self, serializer, currency, user):
        data = {
            'user': user.id, 'currency': currency.code,
            'rate': '12.34', 'threshold': 'BELOW'
        }

        serializer_with_data = serializer(data=data)
        is_valid = serializer_with_data.is_valid()
        notification = serializer_with_data.save(user=user, currency=currency)

        assert is_valid is True
        assert notification is not None

    def test_notification_object_is_updated(
            self, serializer, notification, user, currency):
        current_rate = notification.rate
        current_threshold = notification.threshold

        data = {
            'user': user.id, 'currency': currency.code,
            'rate': '99.88', 'threshold': 'BELOW'
        }

        serializer_with_data = serializer(instance=notification, data=data)
        is_valid = serializer_with_data.is_valid()
        updated_notification = serializer_with_data.save(
            user=user, currency=currency)

        assert is_valid is True
        assert current_rate == '12.34'
        assert current_threshold == 'ABOVE'
        assert updated_notification is not None
        assert updated_notification.rate == Decimal('99.88')
        assert updated_notification.threshold == 'BELOW'

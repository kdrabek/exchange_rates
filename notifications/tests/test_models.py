from notifications.models import Notification


def test_creates_valid_notification_model(db, user, currency):
    notification = Notification.objects.create(
        user=user, currency=currency, rate='12.34', threshold='ABOVE'
    )

    assert isinstance(notification, Notification)
    assert notification.user is user
    assert notification.currency is currency
    assert notification.rate == '12.34'
    assert notification.threshold == 'ABOVE'

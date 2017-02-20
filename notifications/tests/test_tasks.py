from decimal import Decimal
from operator import gt, lt

from django.utils import timezone
import mock
import pytest

from django.conf import settings
from django.template.loader import render_to_string

from notifications.tasks import (
    send_notification_email, get_operator, process_user_notifications
)


@pytest.mark.parametrize('threshold, expected_operator', [
    ('ABOVE', gt), ('BELOW', lt)
])
def test_get_operator(threshold, expected_operator):
    assert get_operator(threshold) is expected_operator


@mock.patch('notifications.tasks.send_notification_email')
def test_process_user_notifications_task(
        mock_send_notification_email, user, notification):
    process_user_notifications()

    mock_send_notification_email.assert_called_once_with(notification.id)


@mock.patch('notifications.tasks.send_mail')
def test_send_notification_email_when_eligible(
        mock_send_mail, notification, rate, user):
    notification.rate = rate.rate - Decimal('0.10')
    notification.save()

    send_notification_email(notification.id)
    rendered_msg = render_to_string(
        'mail.html', {'notification': notification, 'rate': rate}
    )
    mock_send_mail.assert_called_once_with(
        subject='Notification',
        message='A text message',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=rendered_msg
    )


@mock.patch('notifications.tasks.send_mail')
def test_send_notification_email_when_condition_not_met(
        mock_send_mail, notification, rate, user):
    notification.rate = rate.rate - Decimal('0.10')
    notification.threshold = 'BELOW'
    notification.save()

    send_notification_email(notification.id)
    assert notification.rate < rate.rate
    assert not mock_send_mail.called


@mock.patch('notifications.tasks.send_mail')
def test_send_notification_email_when_condition_when_not_old_enough(
        mock_send_mail, notification, rate, user):
    notification.last_sent = timezone.now()
    notification.save()

    send_notification_email(notification.id)
    assert not mock_send_mail.called


@mock.patch('notifications.tasks.send_mail')
def test_send_notification_email_when_condition_notification_inactive(
        mock_send_mail, notification, rate, user):
    notification.is_active = False
    notification.save()

    send_notification_email(notification.id)
    assert not mock_send_mail.called
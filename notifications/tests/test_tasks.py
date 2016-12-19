import mock
import pytest

from django.conf import settings
from django.template.loader import render_to_string

from notifications.tasks import send_notification_email


@pytest.fixture
def rendered_msg(notification, rate):
    return render_to_string(
        'mail.html', {'notification': notification, 'rate': rate}
    )


@mock.patch('notifications.tasks.send_mail')
def test_send_notification_email(
        mock_send_mail, notification, rate, user, rendered_msg):
    send_notification_email(notification, rate)

    mock_send_mail.assert_called_once_with(
        subject='Notification',
        message=None,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=rendered_msg
    )

from decimal import Decimal

import mock

from django.conf import settings
from django.template.loader import render_to_string

from notifications.tasks import send_notification_email


@mock.patch('notifications.tasks.send_mail')
def test_send_notification_email(
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

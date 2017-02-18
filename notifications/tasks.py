from operator import gt, lt

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from exchange_rates import app
from authentication.models import User
from notifications.models import Notification
from rates.models import Rate


def get_operator(threshold):
    if threshold == 'ABOVE':
        return gt
    elif threshold == 'BELOW':
        return lt


@app.task
def process_user_notifications():
    for user in User.objects.all():
        for notification in Notification.objects.filter(user=user):
            send_notification_email(notification.id)


def send_notification_email(notification_id):
    notification = Notification.objects.get(id=notification_id)
    last_rate = Rate.objects.filter(currency=notification.currency).order_by(
        'table__date').last()
    operator = get_operator(notification.threshold)
    if operator(last_rate.rate, notification.rate):
        html_message = render_to_string(
            'mail.html', {'notification': notification, 'rate': last_rate}
        )

        send_mail(
            subject='Notification',
            message='A text message',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
            html_message=html_message
        )

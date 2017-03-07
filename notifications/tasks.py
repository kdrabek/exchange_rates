from datetime import datetime, timedelta
from django.utils import timezone
from operator import gt, lt

from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from exchange_rates import app
from authentication.models import User
from notifications.models import Notification
from rates.models import Rate


logger = get_task_logger(__name__)


def get_operator(threshold):
    if threshold == 'ABOVE':
        return gt
    elif threshold == 'BELOW':
        return lt


@app.task
def process_users():
    for user in User.objects.all():
        logger.warning("Publishing process_notifications for user: %s", user.id)
        process_notifications.delay(user_id=user.id)


@app.task
def process_notifications(user_id):
    try:
        user = User.objects.get(pk=user_id)
        for notification in Notification.objects.filter(user=user):
            send_notification_email(notification.id)
    except Exception as e:
        logger.error("Exception occurred: %s", str(e))


def send_notification_email(notification_id):
    notification = Notification.objects.get(id=notification_id)
    last_rate = Rate.objects.filter(currency=notification.currency).order_by(
        'table__date').last()

    if _should_send(last_rate, notification):
        _send_email(notification, last_rate)
        notification.last_sent = datetime.utcnow()
        notification.save()


def _should_send(last_rate, notification):
    now = timezone.now()
    operator = get_operator(notification.threshold)

    old_enough = (
        now - notification.last_sent > timedelta(hours=12) if
        notification.last_sent else True
    )
    condition_met = operator(last_rate.rate, notification.rate)
    return all([old_enough, condition_met, notification.is_active])


def _send_email(notification, last_rate):
    send_mail(
        subject='Notification',
        message='A text message',
        recipient_list=[notification.user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        html_message=render_to_string(
            'mail.html', {'notification': notification, 'rate': last_rate}
        )
    )

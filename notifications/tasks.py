from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from exchange_rates import app
from rates.models import Rate


logger = get_task_logger(__name__)


@app.task
def send_notification_email(notification, rate):
    # rate = Rate.objects.filter(
    #    currency=notification.currency
    # ).order_by('-table__when_fetched')[1]

    html_message = render_to_string(
        'mail.html', {'notification': notification, 'rate': rate}
    )

    send_mail(
        subject='Notification',
        message=None,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[notification.user.email],
        html_message=html_message
    )

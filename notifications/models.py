from django.db import models


class Notification(models.Model):

    THRESHOLD_ABOVE = 'ABOVE'
    THRESHOLD_BELOW = 'BELOW'

    THRESHOLD_CHOICES = (
        (THRESHOLD_ABOVE, 'above'),
        (THRESHOLD_BELOW, 'below')
    )

    user = models.ForeignKey('authentication.User')
    currency = models.ForeignKey('rates.Currency')
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    threshold = models.CharField(max_length=5, choices=THRESHOLD_CHOICES)
    is_active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True)

from django.db import models
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from authentication.models import User


@receiver(models.signals.post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

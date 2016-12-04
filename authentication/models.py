from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(models.Model):

    email = models.EmailField('email', unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '<User email: {0}>'.format(self.email)

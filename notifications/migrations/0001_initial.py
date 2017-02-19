# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-17 14:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rates', '0003_auto_20161113_0717'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=4, max_digits=6)),
                ('threshold', models.CharField(choices=[('ABOVE', 'above'), ('BELOW', 'below')], max_length=5)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rates.Currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
#!/bin/bash

sleep 10
cd exchange_rates
su -m exchange -c "python manage.py makemigrations exchange_rates"
su -m exchange -c "python manage.py migrate"
su -m exchange -c "python manage.py runserver 0.0.0.0:8000"

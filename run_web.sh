#!/bin/bash

sleep 10
echo "Generating migrations"
su -m exchange -c "./manage.py makemigrations exchange_rates"
echo "Applying migrations"
su -m exchange -c "./manage.py migrate"
su -m exchange -c "/usr/local/bin/gunicorn exchange_rates.wsgi:application -w 2 -b :8000"

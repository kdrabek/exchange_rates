#!/bin/bash

su -m exchange -c "./manage.py makemigrations"
su -m exchange -c "./manage.py migrate"
su -m exchange -c "/usr/local/bin/gunicorn exchange_rates.wsgi:application -w 2 -b :8000"

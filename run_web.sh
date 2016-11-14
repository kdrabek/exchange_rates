#!/bin/bash

sleep 10
echo "Generating migrations"
su -m exchange -c "./manage.py makemigrations exchange_rates"
echo "Applying migrations"
su -m exchange -c "./manage.py migrate"
su -m exchange -c "./manage.py runserver 0.0.0.0:8000"

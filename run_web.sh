#!/bin/bash

sleep 10
cd exchange_rates
echo "Generating migrations"
su -m exchange -c "./manage.py makemigrations exchange_rates"
su -m exchange -c "./manage.py makemigrations rates"
echo "Applying migrations"
su -m exchange -c "./manage.py migrate"
su -m exchange -c "./manage.py runserver 0.0.0.0:8000"

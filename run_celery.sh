#!/bin/sh

sleep 10
cd exchange_rates
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m exchange -c "celery worker -A exchange_rates.celeryconf -Q default -n default@%h"

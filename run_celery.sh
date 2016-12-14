#!/bin/sh

sleep 10
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m exchange -c "celery worker -A exchange_rates.celery -Q default -B -n default@%h"

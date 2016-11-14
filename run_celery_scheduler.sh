#!/bin/sh

sleep 10
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m exchange -c "celery -A exchange_rates.celery beat -l info"

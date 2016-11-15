#!/bin/sh

sleep 10
file="celerybeat.pid"

# if [ -f $file ] ; then
#     su -m exchange "rm -rf $file"
# fi
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m exchange -c "celery -A exchange_rates.celery beat -l info"

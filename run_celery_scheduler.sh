#!/bin/sh

sleep 10

file="celerybeat.pid"
# if [ -f $file ] ; then
#     su -m exchange "rm -rf $file"
# fi

su -m exchange -c "celery -A exchange_rates.celery beat -l info"

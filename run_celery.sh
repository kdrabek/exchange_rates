#!/bin/sh

su -m exchange -c "celery worker -A exchange_rates.celery -Q default -B -n default@%h"

#!/bin/sh

# su -m exchange -c "celery worker -A exchange_rates -B -Q rates"
su -m exchange -c "celery worker -A exchange_rates -B -Q rates -n rates@%h"
su -m exchange -c "celery worker -A exchange_rates -B -Q notifications -n notifications@%h"


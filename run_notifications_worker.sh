#!/bin/sh

su -m exchange -c "celery worker -A exchange_rates -B -Q notifications -n notifications@%h  --concurrency 1 -P solo"



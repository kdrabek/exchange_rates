#!/bin/sh

sleep 10  # so that RabbitMQ starts first
su -m exchange -c "celery worker -A exchange_rates -B -Q rates -n rates@%h"



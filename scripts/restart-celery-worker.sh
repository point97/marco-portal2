#!/bin/bash

PIDFILE=$HOME/run/marco_portal2_celery.pid

kill -HUP `cat $PIDFILE`

# Then wait until the next 5 minute mark, and cron will restart it.

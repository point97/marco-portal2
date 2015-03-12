#!/bin/bash

ENV=$HOME/env/marco_portal2
APPDIR=$HOME/code/marco_portal2/prototype/marco
CELERY=$ENV/bin/celery
PIDFILE=$HOME/run/marco_portal2_celery.pid

source $ENV/bin/activate

# Celery worker has to be run from the same directory as manage.py
cd $APPDIR

# Start the worker with the solo pool, so we only have one process
# (to save memory).

celery worker                   \
       --app marco              \
       --quiet                  \
       --pidfile $PIDFILE       \
       --loglevel INFO          \
       --pool=solo &

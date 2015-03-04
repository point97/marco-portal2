#!/bin/sh

# Script to zip up the calendar models for use locally.

source $HOME/env/marco_portal2/bin/activate

dumpfile=marco_calendar_dump-`date -I`.json

# Apps are dumped in the order they appear here.
apps="calendar.calendar calendar.event"

echo "Dumping $apps, just a second"
cd $HOME/webapps/marco_portal2/site
python manage.py dumpdata --natural --indent=4 $apps > $HOME/$dumpfile 2>/dev/null

cd $HOME
gzip -9 $dumpfile

echo All done, get your file with:
echo scp `hostname`:~/$dumpfile.gz .



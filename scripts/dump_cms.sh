#!/bin/sh

# Script to zip up just the wagtail content from the database, for use locally.

cd $HOME
dumpdir=marco_cms_dump-`date -I`
mkdir $dumpdir
cd $HOME/webapps/marco_portal2/site
source $HOME/env/marco_portal2/bin/activate
for app in base data_catalog data_gaps home initial_data menu ocean_stories pages
 do
  echo Dumping $app
  python manage.py dumpdata $app > $HOME/$dumpdir/portal_$app.dump 2>/dev/null
 done

cd $HOME
tar czf $dumpdir.tar.gz $dumpdir
rm -r $dumpdir

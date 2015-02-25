#!/bin/sh

# Script to zip up just the wagtail content from the database, for use locally.

source $HOME/env/marco_portal2/bin/activate

dumpfile=marco_cms_dump-`date -I`.json

# Apps are dumped in the order they appear here.
apps="auth.user auth.group auth.permission wagtailcore wagtailimages base "
apps="$apps data_gaps data_catalog home initial_data menu ocean_stories pages"

echo "Dumping $apps, just a second"
cd $HOME/webapps/marco_portal2/site
python manage.py dumpdata --natural --indent=4 $apps > $HOME/$dumpfile 2>/dev/null

cd $HOME
gzip -9 $dumpfile

echo All done, get your file with:
echo scp `hostname`:~/$dumpfile.gz .

# To restore to a fresh database, it seems that you have to manually delete all
# of the auth.permission objects except the last one (id=215).
# Alternatively, the creation of that last one should go into a data migration,
# it belongs to the feature sharing system ("Can Share Features")

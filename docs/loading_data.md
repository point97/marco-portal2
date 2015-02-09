# Loading data / fixture management

## Purpose

This document outlines the process for loading some reasonable data into 
your development database so you can start testing functionality right away.

Some data are static files (e.g. media, file-based spatial data, utfgrid json files, etc)
 that the application expects to live at some file path but are too big to be managed comfortably in the repository.

It's not a perfect setup; see the "Concerns" section below for discussion.

## Prereqs

If you're starting on a shiny new dev environment, make sure you've created and
migrated your data schema:

```
scripts/reset_db marco_portal
dj migrate
```

If you can run this, you're good to go...

```
psql -d marco_portal -U postgres 
```

## Data 


### Content

The first step should be loading up the portal data from the Wagtail content management system. This contains "Ocean Stories" and other content critical for site functionality. 
The json fixture should already be in the repo.

```
dj loaddata marco_site/fixtures/content.json
```

To load these fixtures into an existing database you may have to run:

```
from wagtail.wagtailcore.models import *
Page.objects.all().delete()

from wagtail.wagtailsearch.models import *
Query.objects.all().delete()

from portal.base.models import *
PortalRendition.objects.all().delete()
```

**To recreate the content fixture** from prod/stage environments, see below. 
Ideally we could exclude more apps to make this fixture as minimal as possible 
but, for now, it works reliably. Beware that the `contrib.auth` users data is included
due to the dependency with user-owned content!

```
python manage.py dumpdata --exclude data_manager \
    --exclude contenttypes --exclude auth.Permission \
    --exclude sessions --exclude admin --exclude scenarios \
    --natural --indent=2 > content.json

# replace all passwords with "foobar"
perl -pi -e 's/^(\s*"password":\s*")[^"]*(",\s*)$/\1pbkdf2_sha256\$15000\$9mX9qOxjyv3V\$TyVXAst+8rdc2RJLIIlDpXDW+ZuRV8G9+gM2GIz8LYE=\2/g;' content.json
```

### Data Manager

The `data_manager` controls the layers available in the planner map. It is maintained
as a separate fixture as it's typically managed through different means than the 
site content.

```
dj loaddata marco_site/fixtures/data_manager.json
```

### Media

Pull the media directly from prod/stage to your dev environment using rsync (no need to maintain a separate zip file)

```
rsync -avz point97@midatlantic.point97.io:webapps/marco_portal2_media/ media/
```

### Lease blocks

Lease blocks are a multipolygon geospatial dataset with attributes pertaining 
to wind energy, etc. 

```
dj loaddata marco_site/fixtures/scenarios_leaseblocks_3857.json.gz
```

The lineage of this data is somewhat complicated. There is an original shp, a
generated geojson and a django fixture. The django fixture above comes from v1 and was transformed to web mercator projection directly in postgres using the `ST_TRANSFORM` postgis function. Contact @sfletche for additional details.

### UTFGrids

The `utfgrid` static files are critical for map interactivity. The full set of 
data layers amounts to > 5 GB of static files, most of which are at detailed zoom
levels that you'll never hit. You can choose to grab the full set or a subset that
includes all layers but omits zoom levels > 9. 

```
cd marco-portal2/static/data_manager

# Use the subset
cd marco_site/fixtures
curl http://midatlantic.point97.io/static/data_manager/utfgrid_subset.tar.gz
cd ../../static
tar -xzvf ../marco_site/fixtures/utfgrid_subset.tar.gz  
```

**Or** download the big mama, make sure you've got at least 6 GB of space free!

```
# Use the subset
cd marco_site/fixtures
curl http://midatlantic.point97.io/static/data_manager/utfgrid_full.tar.gz
cd ../../static
tar -xzvf ../marco_site/fixtures/utfgrid_full.tar.gz  
```

These are not anticipated to change much at all, if ever. 
The full archive is created with `tar -czf` on `<staticroot>/data_manager/utfgrid`. 
The subset is created by running the `scripts/bundle_utfgrid` script on prod/stage.

## Concerns

* Keeping fixtures synced with subsequent changes to the data models is a pain.
 Mostly we just need to remember to recreate the fixtures after running any
 migrations which touch these tables

* Utmost care must be taken to ensure that user's private data does not make it
into fixtures, both for privacy and syncing. Rule of thumb: data in fixtures is 
"curated", doesn't change often and is not tied to a user. *The dumpdata procedure 
for content is in direct violation of this!* But I can't figure out an easy way 
to move content over without also creating the users to which content belongs.

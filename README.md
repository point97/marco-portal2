# MARCO Portal Redesign

This is the top level project for v2 of the MARCO Portal.

## Useful links

 - [Technical Specification](https://docs.google.com/a/pointnineseven.com/document/d/1bTRnrWeFrgjQ6BqYmLdnf8uIE6iPPJKNZQ-E3jsw8Vc/edit)

## Development Setup

```
vagrant up
vagrant ssh
```

At this point, you will have an empty database. You may want to load a production DB dump (see below).

Otherwise, (within the VM:)

```
dj createsuperuser
dj loaddata --app data_manager data_manager_fixture
djrun
```

This will make the app accessible on the host machine as http://localhost:8111/ . The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

### Building assets

To build the assets, you'll need Node.JS installed, either on your host or in Vagrant.

Then, from the project root:

```
cd marco_site/assets
npm install
./node_modules/.bin/gulp
```

## Production Setup

### Dependencies

 - Elasticsearch
 - Redis
 - Postgresql DB

### Configuration

 - Clone the repo
 - Copy `marco_config/settings/local.template.py` as `local.py` and customize.
 - `pip install --src ./deps -r requirements.txt`
 - createsuperuser
 - `DJANGO_SETTINGS_MODULE="marco_config.settings.production" ./manage.py migrate update_index createsuperuser`

#### Static assets

 - **for now**, rsync marco_site/static/ from your development instance (or run gulp from that dir on the server, if node is available)
 - Run `DJANGO_SETTINGS_MODULE="marco_config.settings.production" ./manage.py compress collectstatic`

## Getting production data

`pg_dump -U marco_portal marco_portal > dump.pg` (password from local.py)

`rsync -avz point97@midatlantic.point97.io:webapps/marco_portal2/site/dump.pg ./`

drop/create

`psql -U postgres marco_portal < dump.pg`

## Used technologies

  * [Openlayers 3](http://openlayers.org/)
  * [Bootstrap 3](http://getbootstrap.com/)
  * [Wagtail](http://wagtail.io/)
  * [Django 1.7](https://docs.djangoproject.com/en/1.7/)

## Candidate Technologies

#### Animation

 - http://greensock.com/tweenlite/

#### Icons

 - https://icomoon.io
 - https://www.npmjs.org/package/icomoon-build

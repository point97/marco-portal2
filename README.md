## Used technologies

  * [Openlayers 3](http://openlayers.org/)
  * [Bootstrap 3](http://getbootstrap.com/)
  * [Wagtail](http://wagtail.io/)
  * [Django 1.7](https://docs.djangoproject.com/en/1.7/)

## Development Setup

```
vagrant up
vagrant ssh
(then, within the SSH session:)
dj createsuperuser
dj loaddata --app data_manager data_manager_fixture
djrun
```

This will make the app accessible on the host machine as http://localhost:8111/ . The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

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

## Candidate Technologies

#### Animation

 - http://greensock.com/tweenlite/

#### Icons

 - https://icomoon.io
 - https://www.npmjs.org/package/icomoon-build

## Portal Integration with Marine Planner

We have two major branches of MARCO MP: the currently deployed Django 1.4 "monolithic" branch, and an in-progress "modular" branch, which breaks MP into ~15 modules and targets Django 1.7. Given the tight timeline to the MARCO Portal soft launch (mid January) we don't believe we'll have time to get the modular branch ready. Therefore, we will launch with the current MP branch, running in a seperate Python process, with the following points of integration between the Portal and MP services:

 - Sign in
  - Only MP. Possibly leave off the signed in element from the portal top menu, unless an easy way presents.
 - Header/footer
  - Portal exposes header as URL which MP curls+caches in redis, then inlines. Footer not needed by MP
 - Styles/assets
  - MP includes from Portal
 - Active layers, data catalog
  - MP exposes API endpoints, needs more detail

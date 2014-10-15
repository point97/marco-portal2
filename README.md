## Used technologies

 * [Django 1.7](https://docs.djangoproject.com/en/1.7/)
 * [Wagtail](http://wagtail.io/)
 * [Openlayers 3](http://openlayers.org/)
 * [Web Starter Kit](https://github.com/point97/web-starter-kit)

## Setup

    vagrant up
    vagrant ssh
      (then, within the SSH session:)
    dj createsuperuser
    djrun

This will make the app accessible on the host machine as http://localhost:8111/ . The codebase is located on the host
machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

## Candidate Technologies

#### Animation

 - http://greensock.com/tweenlite/

#### Icons

 - http://fortawesome.github.io/Font-Awesome/
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

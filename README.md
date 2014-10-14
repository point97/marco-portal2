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


This will make the app accessible on the host machine as http://localhost:8111/ . The codebase is located on the host machine, exported to the VM as a shared folder; code editing and Git operations will generally be done on the host.

## Working with styles

This project includes a style guide, published at [point97.github.io/marco-portal2](http://point97.github.io/marco-portal2/). When changing styles, be sure to update the style guide using the following steps:

### Setup

 - `cd styleguide`
 - `npm install`
 - add `node_modules/.bin` to your `$PATH` so you can just run `gulp`. Otherwise replace `gulp` with `node_modules/.bin/gulp` in the commands below.

### Workflow

 - run `gulp serve`. This will start an auto-reloading webserver using [BrowserSync](http://www.browsersync.io/).
 - Make any style changes and make sure that they are reflected in the appropriate section of the styleguide. CSS classes should follow the [SUIT conventions](https://github.com/suitcss/suit/blob/master/doc/naming-conventions.md) used by [Web Starter Kit](https://developers.google.com/web/starter-kit/).

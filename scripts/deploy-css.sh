#!/bin/bash

# Deploy CSS-only changes to sandbox

set -e

# Figure out where we live on disk
HERE="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
pushd .

ASSETS_DIR=$HERE/../marco_site/assets
STATIC_DIR=$HERE/../static

SANDBOX_STATIC=midatlantic-sandbox.point97.io:/home/point97/webapps/marco_portal2/site/marco_site/static

if [ -z `which npm` ]; then
    echo npm not found in your path. 
    echo Install npm or reconfigure your path and try again.
    exit -1
fi


# Run NPM install and Gulp
cd $ASSETS_DIR
npm install
./node_modules/.bin/gulp

scp $STATIC_DIR/css/marco_site.css $SANDBOX_STATIC/css
scp $STATIC_DIR/css/marco_site.css.map $SANDBOX_STATIC/css

popd


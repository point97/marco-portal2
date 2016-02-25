#!/bin/bash
PROJECT_NAME=$1
APP_NAME=$2

PROJECT_DIR=~/$PROJECT_NAME
VIRTUALENV_DIR=~/.virtualenvs/$PROJECT_NAME

APP_DB_NAME=$3

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip

# # Dependencies for OpenCV image feature detection
# apt-get install -y python-opencv python-numpy

# Virtualenv setup for project
echo "setting up virtualenvs"
/usr/local/bin/virtualenv --system-site-packages $VIRTUALENV_DIR && \
    source $VIRTUALENV_DIR/bin/activate && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    cd $PROJECT_DIR && \
    echo "installing project dependencies"
    $PIP install --src ./deps -r dev_requirements.txt && \
    $PIP install -e $PROJECT_DIR/apps/madrona-analysistools && \
    $PIP install -e $PROJECT_DIR/apps/madrona-features && \
    $PIP install -e $PROJECT_DIR/apps/madrona-forms && \
    $PIP install -e $PROJECT_DIR/apps/madrona-scenarios && \
    $PIP install -e $PROJECT_DIR/apps/madrona-manipulators && \
    $PIP install -e $PROJECT_DIR/apps/mp-clipping && \
    $PIP install -e $PROJECT_DIR/apps/mp-drawing && \
    $PIP install -e $PROJECT_DIR/apps/mp-explore && \
    $PIP install -e $PROJECT_DIR/apps/mp-accounts && \
    $PIP install -e $PROJECT_DIR/apps/mp-visualize && \
    $PIP install -e $PROJECT_DIR/apps/mp-data-manager && \
    $PIP install -e $PROJECT_DIR/apps/mp-proxy && \
    $PIP install -e $PROJECT_DIR/apps/marco-map_groups && \
    $PIP install -e $PROJECT_DIR/apps/p97-nursery && \
    $PIP install -e $PROJECT_DIR/apps/p97settings

echo "workon $PROJECT_NAME" >> /home/vagrant/.bashrc

echo "resetting DB"
$PROJECT_DIR/scripts/reset_db $3

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/$APP_NAME/manage.py

# Run syncdb/migrate/update_index
echo "database syncing and migrations"
$PYTHON $PROJECT_DIR/$APP_NAME/manage.py makemigrations && \
$PYTHON $PROJECT_DIR/$APP_NAME/manage.py migrate --noinput && \
$PYTHON $PROJECT_DIR/$APP_NAME/manage.py update_index

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> ~/.bashrc
alias dj="$PYTHON $PROJECT_DIR/$APP_NAME/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"
EOF
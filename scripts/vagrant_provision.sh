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
/usr/local/bin/virtualenv --system-site-packages $VIRTUALENV_DIR && \
    source $VIRTUALENV_DIR/bin/activate && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    cd $PROJECT_DIR && \
    $PIP install --src ./deps -r requirements.txt

echo "workon $PROJECT_NAME" >> /home/vagrant/.bashrc

$PROJECT_DIR/scripts/reset_db $3

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/$APP_NAME/manage.py

# Run syncdb/migrate/update_index
$PYTHON $PROJECT_DIR/$APP_NAME/manage.py migrate --noinput && \
$PYTHON $PROJECT_DIR/$APP_NAME/manage.py update_index

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> ~/.bashrc
alias dj="$PYTHON $PROJECT_DIR/$APP_NAME/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"
EOF
#!/bin/bash

PROJECT_NAME=$1

PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

APP_DB_NAME=$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip

# TODO: this should be in the base image
apt-get install -y postgresql-9.3-postgis-2.1

# Dependencies for OpenCV image feature detection
apt-get install -y python-opencv python-numpy

# Virtualenv setup for project
su - vagrant -c "/usr/local/bin/virtualenv --system-site-packages $VIRTUALENV_DIR && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache $PIP install -r $PROJECT_DIR/requirements.txt"

echo "workon $PROJECT_NAME" >> /home/vagrant/.bashrc

$PROJECT_NAME/scripts/reset_db $PROJECT_NAME

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# Run syncdb/migrate/update_index
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput && \
                 $PYTHON $PROJECT_DIR/manage.py update_index"

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
alias dj="$PYTHON $PROJECT_DIR/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"
EOF

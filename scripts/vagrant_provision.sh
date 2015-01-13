#!/bin/bash

PROJECT_NAME=$1

PROJECT_DIR=~/$PROJECT_NAME
VIRTUALENV_DIR=~/.virtualenvs/$PROJECT_NAME

APP_DB_NAME=$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip

# # Dependencies for OpenCV image feature detection
# apt-get install -y python-opencv python-numpy

# Virtualenv setup for project
/usr/local/bin/virtualenv --system-site-packages $VIRTUALENV_DIR && \
    source $VIRTUALENV_DIR/bin/activate && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    ssh-keyscan -H bitbucket.org >> ~/.ssh/known_hosts && \
    cd $PROJECT_DIR && \
    $PIP install --src ./deps -r requirements.txt

echo "workon $PROJECT_NAME" >> /home/vagrant/.bashrc

# $PROJECT_NAME/scripts/reset_db $PROJECT_NAME

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# Run syncdb/migrate/update_index
$PYTHON $PROJECT_DIR/manage.py migrate --noinput && \
$PYTHON $PROJECT_DIR/manage.py update_index

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> ~/.bashrc
alias dj="$PYTHON $PROJECT_DIR/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"
EOF

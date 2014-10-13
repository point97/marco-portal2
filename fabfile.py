from fabric.api import *


env.roledefs = {
    'app': [],
}


@roles('app')
def deploy():
    # Remove this line when you're happy that this Fabfile is correct
    raise RuntimeError("Please check the fabfile before using it")

    base_dir = '/usr/local/django/marco_portal'
    virtualenv_dir = '/usr/local/django/virtualenvs/marco_portal'
    python = virtualenv_dir + '/bin/python'
    pip = virtualenv_dir + '/bin/pip'

    supervisor_task = 'marco_portal'

    with cd(base_dir):
        run('git pull origin master')
        run(pip + ' install -r requirements.txt')
        run(python + ' marco_portal/manage.py migrate --settings=marco_portal.settings.production --noinput')
        run(python + ' marco_portal/manage.py collectstatic --settings=marco_portal.settings.production --noinput')
        run(python + ' marco_portal/manage.py compress --settings=marco_portal.settings.production')
        run(python + ' marco_portal/manage.py update_index --settings=marco_portal.settings.production')

    sudo('supervisorctl restart ' + supervisor_task)

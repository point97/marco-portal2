"""WSGI File for Web482
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marco.settings")
activate_this = os.path.expanduser('~/env/marco_portal2/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

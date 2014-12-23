from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required

@permission_required('wagtailadmin.access_admin')
def styleguide(request, template='marco_site/styleguide.html'):
    return render_to_response(template, RequestContext(request, {}))

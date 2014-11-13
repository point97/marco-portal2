from django.shortcuts import render_to_response
from django.template import RequestContext

def styleguide(request, template='marco_site/styleguide.html'):
    return render_to_response(template, RequestContext(request, {}))

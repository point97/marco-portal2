# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from data_manager.models import *

def theme_query():
    return Theme.objects.filter(visible=True).extra(
        select={
            'layer_count': "SELECT COUNT(*) FROM data_manager_layer_themes as mm LEFT JOIN data_manager_layer as l ON mm.layer_id = l.id WHERE mm.theme_id = data_manager_theme.id AND l.layer_type != 'placeholder'"
        }
    )

def index(request):
    template='data_catalog/index.html'
    themes = theme_query()

    return render_to_response(template, RequestContext(request, {'themes': themes}))

def detail(request, theme_slug):

    theme = get_object_or_404(theme_query(), name=theme_slug)
    template = 'data_catalog/detail.html'

    layers = theme.layer_set.exclude(layer_type='placeholder').order_by('name').select_related('parent');

    return render_to_response(template, RequestContext(request, {
        'theme': theme,
        'layers': layers,
    }));

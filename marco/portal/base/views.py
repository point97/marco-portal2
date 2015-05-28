from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from wagtail.wagtailcore import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.index import get_indexed_models
from wagtail.wagtailsearch.backends import get_search_backend

from data_manager.models import Layer, Theme

def search(request, template=settings.WAGTAILSEARCH_RESULTS_TEMPLATE):
    query_string = request.GET.get('q', '')

    if query_string != '':
        wagtail_search_results = []
        theme_results = []
        layer_results = []
        s = get_search_backend()
        models = get_indexed_models()
        models.remove(Page)

        # search themes from data_catalog
        for theme in Theme.objects.filter(visible=True, display_name__icontains=query_string):
            theme_results.append(theme)

        # search layers from data_catalog   
        layer_results.extend(Layer.objects.exclude(layer_type='placeholder').filter(name__icontains=query_string))

        # search wagtail pages
        for item in models:
            results = s.search(query_string, item)
            wagtail_search_results.extend(results)
                
    else:
        wagtail_search_results = None
        theme_results = None
        layer_results = None

    return render_to_response(template, RequestContext(request, {
        'wagtail_search_results': wagtail_search_results,
        'theme_results': theme_results,
        'layer_results': layer_results
    }));
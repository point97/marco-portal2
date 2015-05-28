from django import template
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from wagtail.wagtailcore import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsearch.index import get_indexed_models
from wagtail.wagtailsearch.backends import get_search_backend

from portal.base.models import PortalImage
from portal.ocean_stories.models import OceanStory, OceanStories
from portal.calendar.models import Event
from portal.news.models import News, Story

from data_manager.models import Layer, Theme

register = template.Library()

def search(request, template=settings.WAGTAILSEARCH_RESULTS_TEMPLATE):
    query_string = request.GET.get('q', '')

    ocean_story_results = []
    calendar_news_results = []
    data_needs_results = []
    resources_results = []
    theme_results = []
    layer_results = []

    if len(query_string) >= 2:
        s = get_search_backend()
        models = get_indexed_models()
        # remove unnecessary models
        for i in [Page, Image, PortalImage]:
            models.remove(i)

        # search wagtail pages
        for model in models:
            results = s.search(query_string, model)
            for item in results:
                if isinstance(item, (OceanStory, OceanStories)):
                    ocean_story_results.append(item)
                elif isinstance(item, (Event, News, Story)):
                    calendar_news_results.append(item)
                elif '/data-needs-and-priorities/' in item.url:
                    data_needs_results.append(item)
                elif '/resources/' in item.url:
                    resources_results.append(item)

        # search themes from data_catalog
        for theme in Theme.objects.filter(visible=True, display_name__icontains=query_string):
            theme_results.append(theme)

        # search layers from data_catalog   
        layer_results.extend(Layer.objects.exclude(layer_type='placeholder').filter(name__icontains=query_string))

    return render_to_response(template, RequestContext(request, {
        'ocean_story_results': ocean_story_results,
        'calendar_news_results': calendar_news_results,
        'data_needs_results': data_needs_results,
        'resources_results': resources_results,
        'theme_results': theme_results,
        'layer_results': layer_results
    }));
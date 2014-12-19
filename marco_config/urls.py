import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from django.views.generic.base import RedirectView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap

admin.autodiscover()


# Register search signal handlers
from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as wagtailsearch_register_signal_handlers
wagtailsearch_register_signal_handlers()


urlpatterns = patterns('',
    url('^sitemap\.xml$', sitemap),

    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^data-catalog/', include('portal.data_catalog.urls')),
    url(r'^data_manager/', include('data_manager.urls')),
    url(r'^styleguide/$', 'marco_site.views.styleguide', name='styleguide'),
    url(r'^visualize/', include('visualize.urls')),
    url(r'^mp_profile/', include('mp_profile.urls')),
    url(r'^features/', include('features.urls')),
    url(r'^scenario/', include('scenarios.urls')),
    url(r'^drawing/', include('drawing.urls')),

    url(r'', include(wagtail_urls)),

)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))

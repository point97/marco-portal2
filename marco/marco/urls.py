import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from django.views.generic.base import RedirectView, TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap
from wagtail.wagtailimages import urls as wagtailimages_urls

import mapgroups.urls
import accounts.urls
import explore.urls

admin.autodiscover()


# Register search signal handlers
from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as wagtailsearch_register_signal_handlers
wagtailsearch_register_signal_handlers()


urlpatterns = patterns('',
    url('^sitemap\.xml$', sitemap),

    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^rpc$', 'rpc4django.views.serve_rpc_request'),

    # https://github.com/omab/python-social-auth/issues/399
    # I want the psa urls to be inside the account urls, but PSA doesn't allow
    # nested namespaces. It will likely be fixed in 0.22
    url('^account/auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^account/', include(accounts.urls.urls(namespace='account'))),
    url(r'^g/', include(mapgroups.urls.urls(namespace='groups'))),
    url(r'^explore/', include('explore.urls')),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # url(r'^data-catalog/', include('portal.data_catalog.urls')),
    url(r'^data-catalog/([A-Za-z0-9_-]+)/$', 'portal.data_catalog.views.theme'),
    url(r'^data_manager/', include('data_manager.urls')),
    url(r'^styleguide/$', 'marco_site.views.styleguide', name='styleguide'),
    url(r'^embed/', include('visualize.urls')),
    url(r'^visualize/', include('visualize.urls')),
    url(r'^features/', include('features.urls')),
    url(r'^scenario/', include('scenarios.urls')),
    url(r'^drawing/', include('drawing.urls')),
    url(r'^proxy/', include('mp_proxy.urls')),

    url(r'^join/', TemplateView.as_view(template_name="welcome_snippet/welcome_landing_page.html")),

    url(r'^images/', include(wagtailimages_urls)),
    url(r'', include(wagtail_urls)),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

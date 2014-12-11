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
    
    # https://github.com/omab/python-social-auth/issues/399
    # I want the psa urls to be inside the account urls, but PSA doesn't allow
    # nested namespaces. It will likely be fixed in 0.22
    url('^account/auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^account/', include('accounts.urls', namespace='account')),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^data_manager/', include('data_manager.urls')),
    url(r'^styleguide/$', 'marco_site.views.styleguide', name='styleguide'),
    url(r'^visualize/', include('visualize.urls')),
    url(r'^mp_profile/', include('mp_profile.urls')),

    # this is a temporary measure since data_manager
    # has local layer paths starting with /media/
    url(r'^media/(?P<path>.*)',
        RedirectView.as_view(url='/static/%(path)s'),
        name="cloud_browser_index"),

    url(r'', include(wagtail_urls)),

)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))

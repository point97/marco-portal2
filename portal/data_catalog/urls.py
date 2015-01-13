from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('',
    (r'^$', views.catalog),
    (r'^([A-Za-z0-9_-]+)/$', views.theme),
)

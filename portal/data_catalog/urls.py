from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^([A-Za-z0-9_-]+)/$', views.detail),
)

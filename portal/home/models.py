from django.db import models

from wagtail.wagtailcore.models import Page


class HomePage(Page):
    parent_page_types = []

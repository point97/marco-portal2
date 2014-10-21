from django.db import models

from wagtail.wagtailcore.models import Page as WagtailPage
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class Page(WagtailPage):
    parent_page_types = ['home.HomePage', 'Page']

    body = RichTextField()
    indexed_fields = ('body', )
    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]

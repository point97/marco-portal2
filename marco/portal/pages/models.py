from django.db import models

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index

from portal.base.models import PageBase

class Page(PageBase):

    body = RichTextField()
    search_fields = PageBase.search_fields + (
        index.SearchField('body'),
    )
    content_panels = PageBase.content_panels + [
        FieldPanel('body', classname="full"),
    ]

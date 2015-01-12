from django.db import models

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from portal.base.models import PageBase

class Page(PageBase):

    body = RichTextField()
    search_fields = PageBase.search_fields + ('body',)
    content_panels = PageBase.content_panels + [
        FieldPanel('body', classname="full"),
    ]

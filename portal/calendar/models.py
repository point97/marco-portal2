from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel

class Calendar(Page):
    subpage_types = ['Event']

class Event(Page):
    parent_page_types = ['Calendar']
    subpage_types = []

    description = models.TextField()
    date = models.DateField()

    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
        index.FilterField('date'),
    )
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('description'),
            FieldPanel('date'),
        ], "Event")
    ]


# Get future events which contain the string "Christmas" in the title or description
# >>> EventPage.objects.filter(date__gt=timezone.now()).search("Christmas")

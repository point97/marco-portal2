from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel

class DataGaps(Page):
    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
    )

    description = RichTextField()
    subpage_types = ['DataGap']

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('description'),
        ], 'Data Gaps Page')
    ]

class DataGap(Page):
    parent_page_types = ['DataGaps']
    subpage_types = []

    description = RichTextField()

    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
    )
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('description'),
        ], 'Data Gap')
    ]


# Get future events which contain the string "Christmas" in the title or description
# >>> EventPage.objects.filter(date__gt=timezone.now()).search("Christmas")

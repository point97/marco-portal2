from datetime import date

from django.db import models
from django.db.models import Q

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image

class Event(Page):
    parent_page_types = ['Calendar']
    subpage_types = []

    description = RichTextField()

    feature_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    location = models.TextField(null=True, blank=True, max_length=1024)

    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
        index.FilterField('date'),
    )
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('description'),
            FieldPanel('date'),
            FieldPanel('end_date'),
            FieldPanel('location'),
        ], "Event")
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feature_image'),
    ]


class Calendar(Page):
    subpage_types = ['Event']

    def events(self):
        # Get list of live event pages that are descendants of this page
        events = Event.objects.live().child_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        events = events.filter(Q(end_date__gte=date.today()) | Q(Q(end_date__isnull=True), Q(date__gte=date.today())))

        # Order by date
        events = events.order_by('date')

        return events

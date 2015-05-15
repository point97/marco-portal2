from datetime import date

from django.db import models
from django.db.models import Q

from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel

from portal.base.models import PageBase,DetailPageBase

class Event(DetailPageBase):
    parent_page_types = ['Calendar']

    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.TextField(null=True, blank=True, max_length=1024)

    search_fields = DetailPageBase.search_fields + (
        index.SearchField('description'),
        index.FilterField('date'),
    )
    content_panels = DetailPageBase.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('end_date'),
            FieldPanel('location'),
        ], "Event")
    ]

class Calendar(PageBase):
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

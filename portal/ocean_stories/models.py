from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel
from modelcluster.fields import ParentalKey


# The abstract model for ocean story sections, complete with panels
class OceanStorySectionBase(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    map_state = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('body', classname="full"),
        FieldPanel('map_state'),
    ]

    class Meta:
        abstract = True

# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add sections to (OceanStory)
class OceanStorySection(Orderable, OceanStorySectionBase):
    page = ParentalKey('OceanStory', related_name='sections')

class OceanStories(Page):
    subpage_types = ['OceanStory']

class OceanStory(Page):
    parent_page_types = ['OceanStories']
    subpage_types = []

OceanStory.content_panels = [
    FieldPanel('title'),
    InlinePanel( OceanStory, 'sections', label="Story Sections" ),
]

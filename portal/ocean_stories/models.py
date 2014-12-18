from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel,MultiFieldPanel
from modelcluster.fields import ParentalKey
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image

from django.core.exceptions import ValidationError
import json

import re

try: from urlparse import urlparse
except ImportError: from urllib.parse import urlparse

try: from urllib import unquote
except ImportError: from urllib.parse import unquote

# The abstract model for ocean story sections, complete with panels
class OceanStorySectionBase(models.Model):
    title = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)
    map_state = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('body', classname="full"),
        FieldPanel('map_state'),
    ]

    class Meta:
        abstract = True

    @property
    def parsed_map_state(self):
        if (self.map_state.startswith("http")):
            o = urlparse(self.map_state)
            if o:
                dataLayers = {}
                data = {}
                params = [(unquote(p[0]), unquote(p[1])) for p in [q.split('=') for q in o.fragment.split('&')]]

                for k,v in params:
                    if k == "dls[]":
                        if re.match("^\d+$", v):
                            dataLayers[v] = {};
                    else:
                        data[k] = v
                s = {
                    'view': {
                        'center': (data['x'], data['y']),
                        'zoom': data['z'],
                    },
                    'baseLayer': data['basemap'].replace('+', ' '),
                    'dataLayers': dataLayers,
                }
        else:
            s = json.loads(self.map_state)
        return s

    def clean(self):
        try:
            self.parsed_map_state
        except:
            raise ValidationError({'map_state': 'Invalid map state'})

# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add sections to (OceanStory)
class OceanStorySection(Orderable, OceanStorySectionBase):
    page = ParentalKey('OceanStory', related_name='sections')

class OceanStories(Page):
    subpage_types = ['OceanStory']

    def get_children(self):
        return OceanStory.objects.child_of(self)

class OceanStory(Page):
    parent_page_types = ['OceanStories']
    subpage_types = []

    feature_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def as_json(self):
        try:
            o = {'sections': [ s.parsed_map_state for s in self.sections.all() ]}
        except:
            o = {'sections': []}
        return json.dumps(o);

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feature_image'),
    ]


OceanStory.content_panels = [
    FieldPanel('title'),
    InlinePanel( OceanStory, 'sections', label="Story Sections" ),
]

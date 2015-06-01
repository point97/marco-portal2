from itertools import izip_longest
import json
from data_manager.models import Layer

try:
    import urlparse as parse
except ImportError:
    from urllib import parse

from django.db import models
from django.core.exceptions import ValidationError

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel,MultiFieldPanel
from modelcluster.fields import ParentalKey

from portal.base.models import PageBase, DetailPageBase, MediaItem

def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.
    See: https://docs.python.org/2/library/itertools.html#recipes
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

# The abstract model for ocean story sections, complete with panels
class OceanStorySectionBase(MediaItem):
    title = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)
    map_state = models.TextField()
    map_legend = models.BooleanField(default=False, help_text=("Check to "
       "display the map's legend to the right of the the section text."))

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(MediaItem.panels, "media"),
        FieldPanel('body', classname="full"),
        FieldPanel('map_state'),
        FieldPanel('map_legend'),
    ]

    index_fields = MediaItem.index_fields + (
        'title',
        'body',
    )

    class Meta:
        abstract = True

    def parsed_map_state(self):
        if not self.map_state.startswith("http"):
            return json.loads(self.map_state)

        o = parse.urlparse(self.map_state)
        data_layers = {}
        params = parse.parse_qs(o.fragment)

        dls = params.pop('dls[]', [])

        # dls[]=[true,1,54,true,0.5,42,...] ->
        # dls[] = [(true, 1, 54), (true, 0.5, 42), ...]
        for visible, opacity, layer_id in grouper(dls, 3):
            visible = visible.lower() in ('true', '1')
            opacity = float(opacity)
            try:
                int(layer_id)
            except ValueError:
                # IDs that can't be converted to integers are features, e.g.,
                # 'drawing_aoi_13', which can't be displayed on ocean story
                # maps, so just continue.
                continue

            layer = Layer.objects.filter(id=layer_id)
            layer = layer.values('legend', 'name')

            # layer ID must be a string here
            data_layers[layer_id] = {}
            if not layer:
                continue
            layer = layer[0]

            data_layers[layer_id]['name'] = layer['name']
            data_layers[layer_id]['legend'] = layer['legend']

        s = {
            'view': {
                'center': (params.get('x', [-73.24])[0],
                           params.get('y', [38.93])[0]),
                'zoom': params.get('z', [7])[0],
            },
            'url': self.map_state,
            'baseLayer': params.get('basemap', ['Ocean'])[0],
            'dataLayers': data_layers,
        }

        return s

    def clean(self):
        super(OceanStorySectionBase, self).clean()
        try:
            self.parsed_map_state()
        except Exception as e:
            raise ValidationError({'map_state': 'Invalid map state'})

# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add sections to (OceanStory)
class OceanStorySection(Orderable, OceanStorySectionBase):
    page = ParentalKey('OceanStory', related_name='sections')

class OceanStories(PageBase):
    subpage_types = ['OceanStory']

    search_fields = (index.SearchField('description'),)

    def get_detail_children(self):
        return OceanStory.objects.child_of(self)

class OceanStory(DetailPageBase):
    parent_page_types = ['OceanStories']

    hook = models.CharField(max_length=256, blank=True, null=True)
    explore_title = models.CharField(max_length=256, blank=True, null=True)
    explore_url = models.URLField(max_length=4096, blank=True, null=True)

    search_fields = DetailPageBase.search_fields + (
        index.SearchField('description'),
        index.SearchField('hook'),
        index.SearchField('get_sections_search_text'),
    )

    def as_json(self):
        # try:
        o = {'sections': [s.parsed_map_state() for s in self.sections.all()]}
        # except:
        # o = {'sections': []}
        return json.dumps(o)


OceanStory.content_panels = DetailPageBase.content_panels + [
    MultiFieldPanel([FieldPanel('hook'), FieldPanel('explore_title'), FieldPanel('explore_url')], "Map overlay"),
    InlinePanel( OceanStory, 'sections', label="Sections" ),
]

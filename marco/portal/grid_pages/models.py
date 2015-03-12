from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, \
    MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailsearch import index

from portal.base.models import PageBase, DetailPageBase, MediaItem


# The abstract model for ocean story sections, complete with panels
class GridPageSectionBase(MediaItem):
    title = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(MediaItem.panels, "media"),
        FieldPanel('body', classname="full"),
    ]

    index_fields = MediaItem.index_fields + (
        'title',
        'body',
    )

    class Meta:
        abstract = True

class GridPageSection(Orderable, GridPageSectionBase):
    page = ParentalKey('GridPageDetail', related_name='sections')



class GridPage(PageBase):
    subpage_types = ['GridPageDetail']

    def get_detail_children(self):
        return GridPageDetail.objects.child_of(self)

class GridPageDetail(DetailPageBase):
    parent_page_types = ['GridPage']

    target_year = models.CharField(max_length=4)

    search_fields = DetailPageBase.search_fields + (
        index.FilterField('target_year'),
    )

    content_panels = DetailPageBase.content_panels + [
        FieldPanel('target_year'),
    ]
GridPageDetail.content_panels += [InlinePanel(GridPageDetail, 'sections',
                                              label="Sections"),]


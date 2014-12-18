from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image

class DataGaps(Page):
    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
    )

    description = RichTextField()
    subpage_types = ['DataGap']

    def get_children(self):
        return DataGap.objects.child_of(self)

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

    feature_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    target_year = models.CharField(max_length=4)

    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
    )
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('target_year'),
            FieldPanel('description'),
        ], 'Data Gap')
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feature_image'),
    ]


# Get future events which contain the string "Christmas" in the title or description
# >>> EventPage.objects.filter(date__gt=timezone.now()).search("Christmas")

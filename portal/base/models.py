from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image

class PageBase(Page):
    is_abstract = True
    class Meta:
        abstract = True

    description = RichTextField(blank=True, null=True)
    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('description'),
        ], 'Page')
    ]

class DetailPageBase(PageBase):
    is_abstract = True
    class Meta:
        abstract = True

    feature_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    subpage_types = []
    content_panels = PageBase.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('feature_image'),
        ], 'Detail')
    ]

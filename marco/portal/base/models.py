from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import AbstractImage, AbstractRendition


# Portal defines its own custom image class to replace wagtailimages.Image,
# providing various additional data fields
# see https://github.com/torchbox/verdant-rca/blob/staging/django-verdant/rca/models.py
class PortalImage(AbstractImage):
    creator = models.CharField(max_length=255, blank=True)
    creator_URL = models.URLField(blank=True)

    search_fields = AbstractImage.search_fields + (
        index.SearchField('creator'),
    )

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=PortalImage)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

class PortalRendition(AbstractRendition):
    image = models.ForeignKey('PortalImage', related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=PortalRendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

class PageSection(models.Model):
    class Meta:
        abstract = True

    index_fields = ()

    def get_search_text(self):
        return '\n'.join(getattr(self, field) for field in self.index_fields)


class MediaItem(PageSection):
    media_position_choices = (
        ('left','left'),
        ('right','right'),
        ('full','full'),
    )
    media_image = models.ForeignKey(
        'base.PortalImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    media_embed_url = models.URLField(blank=True, help_text=(mark_safe("The URL to a "
        "video that you'd like to embed, e.g., https://vimeo.com/121095661.")))
    media_caption = models.CharField(max_length=255, blank=True)
    media_position = models.CharField(max_length=8, choices=media_position_choices, default=media_position_choices[0][0])

    index_fields = PageSection.index_fields + (
        'media_caption',
    )

    panels = [
        ImageChooserPanel('media_image'),
        FieldPanel('media_embed_url'),
        FieldPanel('media_caption'),
        FieldPanel('media_position'),
    ]

    class Meta:
        abstract = True

    def clean(self):
        if self.media_image is not None and self.media_embed_url != '':
            raise ValidationError({'media_image': '', 'media_embed_url': 'Provide either an image or an embed URL, but not both.'})

class PageBase(Page):
    is_abstract = True
    class Meta:
        abstract = True

    description = RichTextField(blank=True, null=True)
    search_fields = Page.search_fields + ( # Inherit search_fields from Page
        index.SearchField('description'),
    )

    def get_sections_search_text(self):
        return '\n'.join(section.get_search_text() for section in self.sections.all())

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            FieldPanel('description'),
        ], 'Page')
    ]

    def portal_next_sibling(self):
        return self.get_next_siblings().live().first() or self.get_siblings().live().first()

    def portal_prev_sibling(self):
        return self.get_prev_siblings().live().first() or self.get_siblings().live().last()

class DetailPageBase(PageBase):
    is_abstract = True
    class Meta:
        abstract = True

    feature_image = models.ForeignKey(
        'PortalImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = (index.SearchField('description'),)

    subpage_types = []
    content_panels = PageBase.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('feature_image'),
        ], 'Detail')
    ]

from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import FieldPanel,MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import AbstractImage, AbstractRendition


# Portal defines its own custom image class to replace wagtailimages.Image,
# providing various additional data fields
class PortalImage(AbstractImage):
    pass


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

    def portal_next_sibling(self):
        return self.get_next_siblings().live().first() or self.get_siblings().live().first()

    def portal_prev_sibling(self):
        return self.get_prev_siblings().live().last() or self.get_siblings().live().last()

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

    subpage_types = []
    content_panels = PageBase.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('feature_image'),
        ], 'Detail')
    ]

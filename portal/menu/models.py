from django.db import models

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel,MultiFieldPanel
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet

# The abstract model, complete with panels
class MenuEntryBase(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255)
    url = models.CharField(null=True, blank=True, max_length=4096)

    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
    ]

    def __unicode__(self):
        return self.title

# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add entries to (Menu)
class MenuEntry(Orderable, MenuEntryBase):
    menu = ParentalKey('Menu', related_name='entries')

@register_snippet
class Menu(models.Model):
    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
    ]

    def __unicode__(self):
        return self.title

Menu.panels = [
    FieldPanel('title'),
    InlinePanel( Menu, 'entries', label="Entries" ),
]

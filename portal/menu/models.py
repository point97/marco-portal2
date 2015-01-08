from django.db import models

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel,MultiFieldPanel,PageChooserPanel
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet

# The abstract model, complete with panels
class MenuEntryBase(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(null=True, blank=True, max_length=255)
    url = models.CharField(null=True, blank=True, max_length=4096)
    show_divider_underneath = models.BooleanField(default=False)

    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('title'),
        PageChooserPanel('page'),
        FieldPanel('url'),
        FieldPanel('show_divider_underneath'),
    ]

    @property
    def destination(self):
        if self.page:
            return self.page.url
        else:
            return self.url
    
    @property
    def text(self):
        if self.title:
            return self.title
        elif self.page:
            return self.page.title
        else:
            return ""

    def __unicode__(self):
        return self.text()

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

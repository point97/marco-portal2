import re

from django.db import models

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel,MultiFieldPanel,PageChooserPanel
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet

class WelcomePageEntry(Orderable):
    welcome_page = ParentalKey('WelcomePage', related_name='wtf')
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

    def external(self):
        pattern = re.compile(r"https?://")
        return pattern.match(self.destination)

    @property
    def text(self):
        return str(self)

    def __str__(self):
        if self.title:
            return self.title + '1'
        elif self.page:
            return self.page.title + '2'
        else:
            return "3"


@register_snippet
class WelcomePage(models.Model):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "%s%s" % (self.title, ' (active)' if self.active else '')

    def save(self, *args, **kwargs):
        if self.active:
            WelcomePage.objects.exclude(id=self.id).update(active=False)
        super(WelcomePage, self).save(*args, **kwargs)

WelcomePage.panels = [
    MultiFieldPanel([
        FieldPanel("title", 'active'),
        FieldPanel('active'),
    ]),
    InlinePanel(WelcomePage, 'wtf', label='Entries')
]

import re

from django.db import models

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel,InlinePanel,MultiFieldPanel,PageChooserPanel
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.fields import RichTextField

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import AbstractImage, AbstractRendition

class WelcomePageEntry(Orderable):
    welcome_page = ParentalKey('WelcomePage', related_name='entries')
    title = models.CharField(null=True, blank=True, max_length=255)
    description = RichTextField(blank=True)
    url = models.CharField(null=True, blank=True, max_length=4096)
    show_divider_underneath = models.BooleanField(default=False)

    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    media_image = models.ForeignKey(
        'base.PortalImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        ImageChooserPanel('media_image'),
        FieldPanel('url'),
        PageChooserPanel('page'),
        FieldPanel('show_divider_underneath'),
    ]

    @property
    def destination(self):
        pattern = re.compile(r"https?://")
        external_url = pattern.match(self.url)

        if self.page:
            return self.page.url
        elif external_url:
            return self.url
        else:
            return "/%s/" % self.url

    def external(self):
        pattern = re.compile(r"https?://")
        return pattern.match(self.destination)

    @property
    def text(self):
        return str(self)

    def __str__(self):
        if self.title:
            return self.title
        elif self.page:
            return self.page.title
        else:
            return ''

@register_snippet
class WelcomePage(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "%s%s" % (self.title, ' (active)' if self.active else '')

    def save(self, *args, **kwargs):
        if self.active:
            WelcomePage.objects.exclude(id=self.id).update(active=False)
        super(WelcomePage, self).save(*args, **kwargs)

WelcomePage.panels = [
    MultiFieldPanel([
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('active'),
    ]),
    InlinePanel(WelcomePage, 'entries', label='Entries')
]

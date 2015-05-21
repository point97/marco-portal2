from django.utils.safestring import mark_safe
import re

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
    url = models.CharField(null=True, blank=True, max_length=4096,
                           help_text=("Note: URLs starting with http:// will "
                                      "open in a new window."))
    show_divider_underneath = models.BooleanField(default=False)
    display_options = models.CharField(max_length=1, default='A', choices=(
        ('A', 'Always display'),
        ('I', 'Display only to logged-in users'),
        ('O', 'Display only to anonymous users'),
    ))

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
        FieldPanel('display_options'),
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
    class Meta:
        ordering = ('footer', 'order',)

    title = models.CharField(max_length=255)
    active = models.BooleanField(default=False, help_text=("To display this "
       "menu, check this box. "))
    footer = models.BooleanField(default=False, help_text=("Select to display "
       "this menu in the footer rather than in the nav bar. The footer has "
       "enough room for four menus."))
    order = models.PositiveSmallIntegerField(default=100, help_text=("The "
        "order that this menu appears. Lower numbers appear first."))

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('active'),
            FieldPanel('footer'),
            FieldPanel('order'),
        ]),
    ]

    def __unicode__(self):
        if self.active:
            active = ''
        else:
            active = '(inactive)'

        if self.footer:
            position = 'Footer'
        else:
            position = 'Navbar'

        s = '%s %d. <b>%s</b> %s' % (position, self.order, self.title, active)
        if not self.active:
            s = "<i style='color:#999'>%s</i>" % s

        return mark_safe(s)

Menu.panels.append(InlinePanel( Menu, 'entries', label="Entries" ))

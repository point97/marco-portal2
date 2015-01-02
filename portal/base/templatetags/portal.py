from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
import re

register = template.Library()

# Retrieves all live pages which are children of the calling page
#for standard index listing
@register.inclusion_tag(
    'portal/components/index_listing.html',
    takes_context=True
)
def index_listing(context, parent_page, item_template):
    items = parent_page.get_children().filter(live=True)
    return {
        'items': items,
        'item_template': item_template,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''

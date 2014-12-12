from django import template

register = template.Library()

# Retrieves all live pages which are children of the calling page
#for standard index listing
@register.inclusion_tag(
    'portal/tags/index_listing.html',
    takes_context=True
)
def index_listing(context, parent_page):
    pages = parent_page.get_children().filter(live=True)
    return {
        'pages': pages,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

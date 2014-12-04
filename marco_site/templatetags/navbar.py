from django import template

register = template.Library()

@register.inclusion_tag(
    'marco_site/tags/navbar.html',
    takes_context=True
)
def navbar(context):
    return {
    }

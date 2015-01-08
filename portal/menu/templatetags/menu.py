from django import template
from portal.menu.models import *

register = template.Library()

@register.inclusion_tag('menu/tags/menu.html', takes_context=True)
def menu(context, id):

    try:
        menu = Menu.objects.get(pk=id)
    except Menu.DoesNotExist:
        return
    
    path = context['request'].path
    active = any([path.startswith(e.url) for e in menu.entries.all()])
    return {
        'menu': menu,
        'active': active,
        'request': context['request'],
    }

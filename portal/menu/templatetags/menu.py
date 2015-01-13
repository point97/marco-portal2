from django import template
from django.template.loader import get_template
from portal.menu.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def menu(context, id, menu_type='dropdown'):
    t = get_template("menu/tags/%s.html" % menu_type)
    try:
        menu = Menu.objects.get(pk=id)
    except Menu.DoesNotExist:
        return ''
    
    path = context['request'].path
    active = any([path.startswith(e.destination) for e in menu.entries.all()])
    return t.render(template.Context({
        'menu': menu,
        'active': active,
        'request': context['request'],
    }))

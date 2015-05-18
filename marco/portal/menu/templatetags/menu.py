from django import template
from django.template.loader import get_template
from portal.menu.models import Menu

register = template.Library()

@register.simple_tag(takes_context=True)
def menus(context, kind='header', menu_type='dropdown'):
    """Template tag to render all available menus.
    """
    t = get_template("menu/tags/%s.html" % menu_type)

    footer = (kind == 'footer')
    menus = Menu.objects.filter(active=True, footer=footer)

    # path = context['request'].path
    # highlighted = any([path.startswith(e.destination) for e in menu.entries.all()])
    highlighted = False
    return t.render(template.Context({
        # 'menu': menu,
        'menus': menus,
        'highlighted': highlighted,
        'request': context['request'],
    }))

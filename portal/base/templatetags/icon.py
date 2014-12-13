from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def icon(name):
    return '<i class="fa fa-%s fa-2x"></i>' % name

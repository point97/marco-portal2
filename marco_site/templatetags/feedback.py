from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def feedback_js():
    if (hasattr(settings, 'FEEDBACK_JS_URL')):
        return '<script type="text/javascript" src="%s"></script>' % (settings.FEEDBACK_JS_URL)
    else: return ''

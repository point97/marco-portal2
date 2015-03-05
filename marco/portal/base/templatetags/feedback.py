from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('portal/tags/feedback.html')
def feedback():
    return {
        'iframe_url': settings.FEEDBACK_IFRAME_URL,
    }

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('portal/tags/ga.html')
def ga():
    return {
        'ga_account': settings.GA_ACCOUNT if hasattr(settings, 'GA_ACCOUNT') else '',
    }

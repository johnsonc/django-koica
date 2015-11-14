from django import template
from koica.utils import sanitize_html

register = template.Library()

@register.filter(is_safe=True)
def remove_pre(value):
    return sanitize_html(value, remove_pre=True)
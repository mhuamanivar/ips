from django import template

register = template.Library()

@register.filter
def format_quantity(value):
    try:
        if value == int(value):
            return int(value)
        else:
            return value
    except (ValueError, TypeError):
        return value

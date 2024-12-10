from django import template

register = template.Library()

@register.filter
def format_status(value):
    """
    Removes underscores and the suffix '_ONLY' from a string.
    """
    if value:
        # Remove '_ONLY' and replace underscores with spaces
        return value.replace('_ONLY', '').replace('_', ' ').capitalize()
    return value

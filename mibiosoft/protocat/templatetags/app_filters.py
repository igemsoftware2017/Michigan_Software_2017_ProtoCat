from django import template

register = template.Library()

@register.filter(name='replace_linebr')
def replace_linebr(value):
    """Replaces all values of line break from the given string with a line space."""
    return value.replace("\n", ' ')

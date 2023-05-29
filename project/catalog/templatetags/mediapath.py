from django import template
from django.conf import settings

register = template.Library()

# Шаблонный фильтр
@register.filter
def mediapath(value):
    return settings.MEDIA_URL + value

# Шаблонный тег
@register.simple_tag
def mediapath(value):
    return settings.MEDIA_URL + value
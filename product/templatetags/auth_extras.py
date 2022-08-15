from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter
def hash(h, key):
    return h[key]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

# apps/minutes/templatetags/minutes_extras.py

from django import template
from django.contrib.auth import get_user_model

register = template.Library()

User = get_user_model()

@register.filter
def user_from_id(user_id):
    """
    Retrieve a User object from a user ID, or return "Unknown User" if not found.
    """
    try:
        return User.objects.get(id=user_id).get_full_name()
    except (User.DoesNotExist, ValueError, TypeError):
        return "Unknown User"


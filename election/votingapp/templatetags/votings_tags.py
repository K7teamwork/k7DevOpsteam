from django import template
from votingapp.models import Vote

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using its key"""
    return dictionary.get(key)

@register.filter
def get_votes(candidate):
    """Get the total votes for a candidate"""
    return Vote.objects.filter(candidate=candidate).count()

@register.filter
def get_total_votes(position):
    """Get the total votes for a position"""
    return Vote.objects.filter(candidate__position=position).count()

@register.filter
def percentage(value, total):
    """Calculate the percentage"""
    if total > 0:
        return round((value / total) * 100, 2)
    return 0
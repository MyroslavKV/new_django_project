from django import template



register = template.Library()

@register.filter
def calculate_discount(value, arg):
    discount = value * arg / 100
    return value - discount
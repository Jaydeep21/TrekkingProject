from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(a,b):
  return a-b
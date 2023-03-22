from django import template

register = template.Library()

@register.filter(name='subtract')
def upper(a,b):
  return a-b
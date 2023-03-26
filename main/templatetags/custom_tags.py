from django import template
from google_currency import convert

register = template.Library()


@register.filter(name='subtract')
def subtract(a,b):
  return a-b


@register.filter
def convert_currency(amount, target_currency):
    return convert('CAD', target_currency, amount)

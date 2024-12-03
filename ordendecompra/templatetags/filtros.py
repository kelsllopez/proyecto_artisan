from django import template
from babel.numbers import format_decimal
register = template.Library()

@register.filter
def moneda(value):
    return format_decimal(value,locale='es_CL')

@register.filter
def monedafix(value):
    return format_decimal(round(value),locale='es_CL')


@register.filter
def arreglarfloat(value):
    return str(value)
from django import template
from babel.numbers import format_decimal
register = template.Library()
from django.conf import settings

@register.filter
def unidades(unidad):
    if unidad in settings.UNIDADES:
        return settings.UNIDADES[unidad]
    return unidad


@register.filter
def arreglar(self):
    return str(self).replace(',','.')


register = template.Library()

@register.filter
def formatoCLP(value):
    return f"${value:,.2f}"  # Ajusta el formato según lo necesites
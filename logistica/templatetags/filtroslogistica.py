from django import template
register = template.Library()

@register.filter
def filtrarRutas(rutas,estado):
    return rutas.filter(estado=estado)
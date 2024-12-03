from django import template
register = template.Library()

@register.filter
def obtenercolumna(columnas,pauta):
    return columnas.filter(pauta_produccion_id=pauta)

@register.filter
def filtrarcolumna(columnas,id_parametro):
    existe = columnas.filter(plantilla_columna_id=id_parametro).first()
    if existe:
        if existe.plantilla_columna.tipo == '3':
            if existe.valor == '1':
                return '<td>Sí</td>'
            else:
                return '<td>No</td>'
        return f"<td>{existe.valor}</td>"
    else:
        return '<td></td>'

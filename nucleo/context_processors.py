from inventario.models import Bodega
from django.conf import settings
def bodegasnav(request):
    bodegasq = Bodega.objects.all()
    bodegas = []
    for bodega in bodegasq:
        lugar = bodega.nombre
        permisoi = 'inventario.inventarioi_{}'.format(lugar.lower().replace(' ','-'))
        permisop = 'inventario.inventariop_{}'.format(lugar.lower().replace(' ','-'))
        bodega = {'lugar': lugar, 'permisoi': permisoi, 'permisop': permisop}
        bodegas.append(bodega)
    return {'bodegasnav': bodegas}


def valoriva(request):
    return {'valorIVA': settings.IVA}

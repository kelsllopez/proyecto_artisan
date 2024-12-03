from .functions import comparar_palabra, historial_actualizar_insumo, historial_actualizar_producto, historial_actualizar_rama, historial_crear_insumo, historial_crear_producto, historial_crear_rama, historial_eliminar_insumo, historial_eliminar_producto, historial_eliminar_rama
from inventario.models import InventarioInsumo
from pauta.models import Pauta
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.static import serve
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponseForbidden
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import InsumoOrdenSerializer, ProductoSerializer, ProveedorInsumoSerializer, RamaSerializer
from nucleo.mixins import ValidatePermissionRequiredMixin
from .models import Insumo, InsumoDirectoProducto, Producto, Rama, Linea, InsumoElaboracionProducto
from proveedores.models import ProveedorInsumo, Proveedor
from .forms import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib import messages


#cargar datos
from clientes.models import Cliente
from nucleo.models import Moneda
from ordendecompra.models import OrdenDeCompra
import pandas as pd
import math
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
# solo usuarios logeados pueden acceder al home
# views.py

import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView
from ordendecompra.models import *
from ventas.models import *

# views.py

import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView


from django.db.models import Sum
# Importaciones necesarias
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.db.models import Sum
from io import BytesIO
# Decorador para asegurar que el usuario esté logueadofrom django.utils import timezone
from django.shortcuts import render
import pandas as pd
import numpy as np
from django.utils import timezone

from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
import pandas as pd
import numpy as np
from django.utils import timezone
from django.db.models import Sum
import numpy as np
import numpy as np
import pandas as pd
from django.db.models import Sum, F
from django.db.models import Avg
from django.db.models import Sum
import pandas as pd


from django.db.models import Sum
from django.views.generic import TemplateView
import pandas as pd
from django.db.models import Sum
import pandas as pd
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "nucleo/a.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener los filtros de fecha y estado (si existen)
        fecha_inicio = self.request.GET.get('fecha_inicio', None)
        fecha_fin = self.request.GET.get('fecha_fin', None)
        estado = self.request.GET.get('estado', None)

        # Inicializar el queryset base para OrdenDeCompra
        ordenes = OrdenDeCompra.objects.all()

        # Filtrar por fecha de inicio y fin
        if fecha_inicio and fecha_fin:
            ordenes = ordenes.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            ordenes = ordenes.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            ordenes = ordenes.filter(fecha__lte=fecha_fin)

        # Filtrar por estado (si se proporciona)
        if estado:
            ordenes = ordenes.filter(estado=estado)

        # Obtener los datos de OrdenDeCompraInsumo
        ordenes_insumos = OrdenDeCompraInsumo.objects.filter(orden__in=ordenes)
        
        # Consultar la suma de los valores netos por cada insumo
        insumos_data = ordenes_insumos.values('insumo__insumo__nombre').annotate(total_neto=Sum('neto'))

        # Convertir los datos de insumos a listas de nombres y valores netos
        insumos_labels = [insumo['insumo__insumo__nombre'] for insumo in insumos_data]
        insumos_values = [insumo['total_neto'] for insumo in insumos_data]

        # Filtrar los productos de venta relacionados con las órdenes de venta producto
        ordenes_venta_productos = OrdenDeVentaProducto.objects.all()

        # Filtrar por fecha si es necesario
        if fecha_inicio and fecha_fin:
            ordenes_venta_productos = ordenes_venta_productos.filter(orden__fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            ordenes_venta_productos = ordenes_venta_productos.filter(orden__fecha__gte=fecha_inicio)
        elif fecha_fin:
            ordenes_venta_productos = ordenes_venta_productos.filter(orden__fecha__lte=fecha_fin)

        # Agrupar los productos vendidos por producto y calcular el precio total
        productos_data = ordenes_venta_productos.values('producto__nombre').annotate(total_precio=Sum('precio'))

        # Convertir los datos de productos a listas de nombres y valores de precio total
        productos_labels = [producto['producto__nombre'] for producto in productos_data]
        productos_values = [producto['total_precio'] for producto in productos_data]

        # Asegúrate de incluir los campos 'fecha' y 'total_neto' en el queryset de OrdenDeCompra
        ordenes_data = ordenes.values('fecha', 'total_neto')  # Incluye 'fecha' y 'total_neto'

        # Convertir las órdenes a un DataFrame para manipularlas
        df = pd.DataFrame(ordenes_data)

        # Verifica si 'fecha' existe antes de convertirla a tipo datetime
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'])

            # Agrupar por fecha y calcular la suma de 'total_neto'
            df_grouped = df.groupby('fecha').agg({'total_neto': 'sum'}).reset_index()

            # Convertir los datos a listas para pasarlos al contexto
            labels = df_grouped['fecha'].dt.strftime('%Y-%m-%d').tolist()  # Formato YYYY-MM-DD
            data = df_grouped['total_neto'].tolist()

            # Pasar los datos y las etiquetas al contexto
            context['labels'] = labels
            context['data'] = data
        else:
            # Si la columna 'fecha' no está en el DataFrame, es posible que no haya datos para ese filtro
            context['labels'] = []
            context['data'] = []

        # Pasar los filtros al contexto
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        context['estado'] = estado

        # Pasar las opciones de estado al contexto
        context['estados'] = OrdenDeCompra._meta.get_field('estado').choices  # Usamos .choices para obtener las opciones de estado

        # Pasar los datos de los insumos y sus valores netos al contexto
        context['insumos_labels'] = insumos_labels
        context['insumos_values'] = insumos_values

        # Pasar los datos de los productos y sus precios totales al contexto
        context['productos_labels'] = productos_labels
        context['productos_values'] = productos_values

        # Nuevos KPIs y cálculos
        # Número de órdenes de compra
        context['numero_ordenes_compra'] = ordenes.count()

        # Total Neto de Insumos por Estado
        total_neto_insumos_por_estado = ordenes_insumos.values('orden__estado').annotate(total_neto=Sum('neto'))
        context['total_neto_insumos_por_estado'] = total_neto_insumos_por_estado

        # Total de ventas de productos
        context['total_ventas'] = sum(productos_values)

        # Rentabilidad de Insumos: Cálculo de la diferencia entre el costo de los insumos y su precio de venta
        insumos_con_precio_venta = ordenes_insumos.values('insumo__insumo__nombre').annotate(
            precio_venta=Sum('insumo__precio'), total_neto=Sum('neto')
        )
        rentabilidad_insumos = [
            (insumo['insumo__insumo__nombre'], insumo['total_neto'] - insumo['precio_venta'])
            for insumo in insumos_con_precio_venta
        ]
        context['rentabilidad_insumos'] = rentabilidad_insumos

        # 1. Total de Órdenes de Compra Pagadas
        context['ordenes_pagadas'] = ordenes.filter(pagada=True).count()

        # 2. Total de Insumos Recibidos
        total_insumos_recibidos = ordenes_insumos.filter(cantidad_recibida__gt=0).aggregate(total=Sum('cantidad_recibida'))['total']
        context['total_insumos_recibidos'] = total_insumos_recibidos if total_insumos_recibidos else 0

        # 3. Cantidad Total Vendida
        total_vendida = ordenes_venta_productos.aggregate(total=Sum('cantidad'))['total']
        context['total_vendida'] = total_vendida if total_vendida else 0

        # 4. Total de Descuento en Ventas
        total_descuento = ordenes_venta_productos.aggregate(total=Sum('descuento'))['total']
        context['total_descuento'] = total_descuento if total_descuento else 0

        # 5. Promedio de Pago por Orden de Compra
        ordenes_pagadas = ordenes.filter(pagada=True)
        if ordenes_pagadas.exists():
            # Crear la lista de tiempos de pago solo si la fecha de pago existe
            tiempos_pago = [(orden.fecha_pago - orden.fecha).days for orden in ordenes_pagadas if orden.fecha_pago]
            
            # Verificar que la lista no esté vacía antes de calcular el promedio
            if tiempos_pago:
                promedio_pago = sum(tiempos_pago) / len(tiempos_pago)
            else:
                promedio_pago = 0  # Si no hay tiempos de pago, el promedio es 0
        else:
            promedio_pago = 0  # Si no hay órdenes pagadas, el promedio es 0

        context['promedio_pago'] = promedio_pago


        return context



from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from datetime import datetime
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.exceptions import ValidationError
def generate_pdf(request):
    # Obtener los filtros de fecha y estado (si existen)
    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)
    estado = request.GET.get('estado', None)

    # Verifica si las fechas están presentes y si tienen un formato válido
    try:
        if fecha_inicio:
            if fecha_inicio.lower() != "none":
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            else:
                fecha_inicio = None
        else:
            fecha_inicio = None

        if fecha_fin:
            if fecha_fin.lower() != "none":
                fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            else:
                fecha_fin = None
        else:
            fecha_fin = None
    except ValueError:
        raise ValidationError("El formato de la fecha es inválido. Debe ser YYYY-MM-DD.")

    # Inicializar el queryset base para OrdenDeCompra
    ordenes = OrdenDeCompra.objects.all()

    # Filtrar por fecha de inicio y fin solo si están presentes
    if fecha_inicio and fecha_fin:
        ordenes = ordenes.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        ordenes = ordenes.filter(fecha__gte=fecha_inicio)
    elif fecha_fin:
        ordenes = ordenes.filter(fecha__lte=fecha_fin)

    # Filtrar por estado solo si está presente
    if estado:
        ordenes = ordenes.filter(estado=estado)

    # Obtener los datos de OrdenDeCompraInsumo
    ordenes_insumos = OrdenDeCompraInsumo.objects.filter(orden__in=ordenes)
    insumos_data = ordenes_insumos.values('insumo__insumo__nombre').annotate(total_neto=Sum('neto'))
    insumos_labels = [insumo['insumo__insumo__nombre'] for insumo in insumos_data]
    insumos_values = [insumo['total_neto'] for insumo in insumos_data]

    # Queryset de OrdenDeVenta
    ordenes_venta = OrdenDeVenta.objects.all()

    # Filtrar por fecha si es necesario
    if fecha_inicio and fecha_fin:
        ordenes_venta = ordenes_venta.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        ordenes_venta = ordenes_venta.filter(fecha__gte=fecha_inicio)
    elif fecha_fin:
        ordenes_venta = ordenes_venta.filter(fecha__lte=fecha_fin)

    # Filtrar los productos de venta relacionados con las órdenes de venta
    ordenes_venta_productos = OrdenDeVentaProducto.objects.filter(orden__in=ordenes_venta)
    productos_data = ordenes_venta_productos.values('producto__nombre').annotate(total_precio=Sum('precio'))
    productos_labels = [producto['producto__nombre'] for producto in productos_data]
    productos_values = [producto['total_precio'] for producto in productos_data]

    # Calcular los KPIs
    numero_ordenes_compra = ordenes.count()

    # Total Neto de Insumos por Estado
    total_neto_insumos_por_estado = ordenes_insumos.values('orden__estado').annotate(total_neto=Sum('neto'))

    # Total de ventas de productos
    total_ventas = sum(productos_values)

    # Rentabilidad de Insumos
    insumos_con_precio_venta = ordenes_insumos.values('insumo__insumo__nombre').annotate(
        precio_venta=Sum('insumo__precio'), total_neto=Sum('neto')
    )
    rentabilidad_insumos = [
        (insumo['insumo__insumo__nombre'], insumo['total_neto'] - insumo['precio_venta'])
        for insumo in insumos_con_precio_venta
    ]

    # Promedio de Pago por Orden de Compra
    ordenes_pagadas = ordenes.filter(pagada=True)
    if ordenes_pagadas.exists():
        tiempos_pago = [(orden.fecha_pago - orden.fecha).days for orden in ordenes_pagadas if orden.fecha_pago]
        promedio_pago = sum(tiempos_pago) / len(tiempos_pago)
    else:
        promedio_pago = 0

    # KPIs de porcentaje
    # Porcentaje de Órdenes Pagadas
    porcentaje_ordenes_pagadas = (ordenes_pagadas.count() / numero_ordenes_compra) * 100 if numero_ordenes_compra > 0 else 0

    # Porcentaje de Rentabilidad de Insumos
    total_rentabilidad_insumos = sum([insumo[1] for insumo in rentabilidad_insumos])
    total_neto_insumos = sum(insumos_values)
    porcentaje_rentabilidad_insumos = (total_rentabilidad_insumos / total_neto_insumos) * 100 if total_neto_insumos > 0 else 0

    # Porcentaje de Ventas de Productos
    porcentaje_ventas_por_producto = [(producto, (valor / total_ventas) * 100) for producto, valor in zip(productos_labels, productos_values)]

    # Contexto para pasar al template
    context = {
        'numero_ordenes_compra': numero_ordenes_compra,
        'total_ventas': total_ventas,
        'total_neto_insumos_por_estado': total_neto_insumos_por_estado,
        'rentabilidad_insumos': rentabilidad_insumos,
        'insumos': zip(insumos_labels, insumos_values),
        'productos': zip(productos_labels, productos_values),
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'estado': estado,  # Pasar el estado para mostrarlo en el PDF
        'promedio_pago': promedio_pago,
        'porcentaje_ordenes_pagadas': porcentaje_ordenes_pagadas,
        'porcentaje_rentabilidad_insumos': porcentaje_rentabilidad_insumos,
        'porcentaje_ventas_por_producto': porcentaje_ventas_por_producto,
    }

    # Renderiza el template HTML
    html_content = render_to_string('nucleo/pdf_template.html', context)

    # Convertir HTML a PDF usando xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="kpi_report.pdf"'

    pisa_status = pisa.CreatePDF(html_content, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response



# -- INSUMOS -- #

# Generación de la api de los insumos para ser consumida por sus vistas
@method_decorator(login_required, 'dispatch')
class InsumoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoOrdenSerializer

    def list(self, request):
        permisos = ['nucleo.insumo.listar', 'nucleo.producto.crear', 'nucleo.producto.actualizar', 'pauta.actualizar', 'pauta.crear']
        check = False
        for p in permisos:
            if self.request.user.has_perm(p):
                check = True
        if check:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("[]")

    @action(detail=True, methods=['get'])
    def proveedores(self, request, pk=None):
        queryset = ProveedorInsumo.objects.filter(insumo=pk).all()
        serializer = ProveedorInsumoSerializer(queryset, many=True)
        return Response(serializer.data)


def validar_rut(rut):
    rut = rut.replace('.','')
    numeros = rut.split('-')[0]
    digito = rut.split('-')[1]
    numeros = f'{int(numeros):,.2f}'.split('.')[0].replace(',','.') +'-'+ digito
    return numeros

# Actualizar Cliente
def actualizar_cliente(request):
    df = pd.read_excel('datos.xlsx')
    proveedores = Proveedor.objects.all()
    # Proveedores
    for i in df.index:
        try:
            razon_social = df['Razon Social'][i]
            rut = validar_rut(df['RUT'][i])
            contacto = df['Contacto Comercial'][i]
            telefono = df['Teléfono contacto'][i]
            mail = df['Mail'][i]
            print(rut,contacto,telefono,mail,razon_social)
            proveedor = [proveedor for proveedor in proveedores if proveedor.empresa_rut == rut]
            if len(proveedor) > 0:
                proveedor = proveedor[0]
                proveedor.ventas_telefono = telefono
                proveedor.ventas_nombre = contacto
                proveedor.save()
        except Exception as ex:
            print(ex)
    return HttpResponse('Holi')

# Actualizar Clientes
def direccion_cliente(request):
    df = pd.read_excel('datosc.xlsx')
    clientes = Cliente.objects.all()
    for i in df.index:
        nombre = df['nombre'][i]
        direccion = df['direccion'][i]
        for cliente in clientes:
            try:
                if cliente.nombre.lower() == nombre.lower():
                    cliente.direccion = direccion
                    cliente.save()
                    local = cliente.clientelocal_set.filter(local="Casa Matriz").first()
                    if local:
                        local.direccion = direccion
                        local.save()
            except Exception as ex:
                print(ex)
    return HttpResponse('holi')
# Cargar Datos
def cargar_datos(request):
    df = pd.read_excel('datos.xlsx')
    insumos = Insumo.objects.all()
    proveedores = Proveedor.objects.all()
    unidad = {'lt': 'Litro', 'u': 'Unidad', 'kg': 'Kilogramo', 'c': 'Caja'}
    creados = 0
    for i in df.index:
        # INSUMO
        try:
            unidad_i = unidad[df['Unidad'][i].lower()]
        except:
            continue
        nombre = df['Materias Primas'][i]
        stock = df['STOCK CRITICO'][i]
        if math.isnan(stock):
            stock = 0
        # ver si el insumo ya existe
        insumo = [insumo for insumo in insumos if insumo.nombre.lower() == nombre.lower() and insumo.unidad == unidad_i]
        # si existe continuamos
        if len(insumo) == 0:
            insumo = Insumo.objects.create(nombre=nombre, unidad=unidad_i, stock_critico=int(stock))
            creados+=1
            insumos = Insumo.objects.all()
        else:
            insumo = insumo[0]
        # Proveedores
        razon_social = df['Razon Social'][i]
        rut = validar_rut(df['RUT'][i])
        contacto = df['Contacto Comercial'][i]
        telefono = df['Teléfono contacto'][i]
        mail = df['Mail'][i]
        proveedor = [proveedor for proveedor in proveedores if proveedor.empresa_rut == rut]
        # si existe seguimos
        if len(proveedor) == 0:
            proveedor = Proveedor.objects.create(empresa_nombre=razon_social, empresa_rut=rut, ventas_nombre=contacto, ventas_email=mail, ventas_celular=telefono)
            proveedores = Proveedor.objects.all()
            creados+=1
        else:
            proveedor = proveedor[0]
        #ASOCIACION
        precio = df['Precio'][i]
        formato = df['FORMATO DE COMPRA'][i]
        lead = df['LEAD TIME'][i]
        divisa = df['INTERNACIONAL'][i]
        if math.isnan(lead) or math.isnan(formato) or math.isnan(precio):
            continue
        #vemos si existe la asociación
        pi = proveedor.proveedorinsumo_set.filter(insumo=insumo,formato=formato).first()
        if pi is None:
            if divisa not in ['EUR','USD']:
                moneda = Moneda.objects.filter(nombre="CLP").first()
            else:
                divisa = divisa.upper()
                moneda = Moneda.objects.filter(nombre=divisa).first()
            pi = proveedor.proveedorinsumo_set.create(insumo=insumo,precio=precio*formato,formato=formato,lead=lead,moneda=moneda,nombre_insumo=insumo.nombre)
            creados+=1
        else:
            pi.precio = precio*formato
            pi.save()
    print(f"se agregaron {creados} insumos/clientes/asociaciones al sistema")
        
    return HttpResponse('Hola :)')



@method_decorator(login_required, 'dispatch')
class InsumoListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "nucleo/insumo-lista.html"

    # permiso necesario
    permission_required = 'nucleo.insumo.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los insumos.'

@method_decorator(login_required, 'dispatch')
class InsumoCreateView(ValidatePermissionRequiredMixin, CreateView):
    template_name = "nucleo/insumo-crear.html"
    model = Insumo
    form_class = InsumoForm
    success_url = reverse_lazy('administrador:insumo:lista')

    # permiso necesario
    permission_required = 'nucleo.insumo.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:insumo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un insumo.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        check = self.request.POST.get('forzar')
        if check is None:
            nombre = form.cleaned_data.get('nombre')
            insumo_ids = [insumo.id for insumo in Insumo.objects.all() if comparar_palabra(nombre, insumo.nombre) > 0.80]
            if len(insumo_ids) > 0:
                insumos = [insumo.nombre for insumo in Insumo.objects.filter(id__in=insumo_ids).all()]
                form.add_error('nombre', "El nombre ya es muy similar a otros ({})".format(' ,'.join(insumos)))
                return super(InsumoCreateView, self).form_invalid(form)
        self.object.save()
        historial_crear_insumo(self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, 'dispatch')
class InsumoUpdateView(UpdateView):
    template_name = "nucleo/insumo-actualizar.html"
    model = Insumo
    form_class = InsumoForm
    success_url = reverse_lazy('administrador:insumo:lista')

    # permiso necesario
    permission_required = 'nucleo.insumo.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:insumo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un insumo.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        check = self.request.POST.get('forzar')
        if check is None:
            nombre = form.cleaned_data.get('nombre')
            insumo_ids = [insumo.id for insumo in Insumo.objects.exclude(pk=self.object.pk).all() if comparar_palabra(nombre, insumo.nombre) > 0.80]
            if len(insumo_ids) > 0:
                insumos = [insumo.nombre for insumo in Insumo.objects.filter(id__in=insumo_ids).all()]
                form.add_error('nombre', "El nombre ya es muy similar a otros ({})".format(' ,'.join(insumos)))
                return super(InsumoUpdateView, self).form_invalid(form)
        # actualizar todos los insumos asociados (para el stock)
        self.object.save()
        insumos = InventarioInsumo.objects.filter(insumo=self.object.id).all()
        for i in insumos:
            i.save()
        historial_actualizar_insumo(self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, 'dispatch')
class InsumoDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'nucleo.insumo.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            insumo = get_object_or_404(Insumo, pk=kwargs.get('pk'))
            historial_eliminar_insumo(self.request.user, insumo)
            insumo.delete()
            return JsonResponse({'estado': 'ok', 'insumo': insumo.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})


# -- FIN INSUMOS -- #

# -- INICIO Areas de Negocio -- #
# Generación de la api de las areas de negocio para ser consumida por sus vistas


@method_decorator(login_required, 'dispatch')
class RamaViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Rama.objects.all()
    serializer_class = RamaSerializer

    # permiso necesario
    permission_required = 'nucleo.rama.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las áreas del negocio.'

    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        queryset = Producto.objects.filter(rama=pk).all()
        serializer = ProductoSerializer(queryset, many=True)
        rama = Rama.objects.filter(pk=pk).first()
        serializer_rama = RamaSerializer(rama)
        return Response({"productos": serializer.data, "rama": serializer_rama.data})

# Lista de las distintas Áreas del negocio


@method_decorator(login_required, 'dispatch')
class RamaListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "nucleo/rama-lista.html"

    # permiso necesario
    permission_required = 'nucleo.rama.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las áreas del negocio.'

@method_decorator(login_required, 'dispatch')
class RamaCreateView(ValidatePermissionRequiredMixin, CreateView):
    # INFO
    template_name = 'nucleo/rama-crear.html'
    model = Rama
    form_class = RamaForm
    success_url = reverse_lazy('administrador:area:lista')

    # PERMISOS #
    permission_required = 'nucleo.rama.crear'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una área de negocio'

    def form_valid(self, form):
        self.object = form.save()
        #obtenemos las lineas de productos
        lineas = self.request.POST.getlist('linea')
        for l in lineas:
            if len(l) > 0:
                self.object.linea_set.create(nombre=l)
        historial_crear_rama(self.request.user, self.object)
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class RamaUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # INFO
    template_name = 'nucleo/rama-actualizar.html'
    model = Rama
    form_class = RamaForm
    success_url = reverse_lazy('administrador:area:lista')

    # PERMISOS #
    permission_required = 'nucleo.rama.actualizar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un área de negocio'

    def form_valid(self, form):
        self.object = form.save()
        # obtenemos las lineas de productos
        lineas = self.request.POST.getlist('linea')
        idlineas = [int(x) for x in self.request.POST.getlist('idlinea')]
        for i, l in enumerate(lineas):
            id = idlineas[i]
            check = Linea.objects.filter(pk=id).first()
            if check:
                check.nombre = l
                check.save()
            else:
                if len(l) > 0 and id == 0:
                    linea = self.object.linea_set.create(nombre=l)
                    idlineas[i] = linea.id
        # eliminamos los que no esten
        [linea.delete() for linea in self.object.linea_set.all() if linea.id not in idlineas]
        historial_actualizar_rama(self.request.user, self.object)
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class RamaDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'nucleo.rama.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            rama = get_object_or_404(Rama, pk=kwargs.get('pk'))
            historial_eliminar_rama(self.request.user, rama)
            rama.delete()
            return JsonResponse({'estado': 'ok', 'rama': rama.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

# FIN AREAS DE NEGOCIO #

# PRODUCTOS #
# Generación de la api de los productos para ser consumida por sus vistas



@method_decorator(login_required, 'dispatch')
class ProductoViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # permiso necesario
    permission_required = 'nucleo.producto.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los productos.'


# Lista de los productos del negocio
# Lista de los productos del negocio
@method_decorator(login_required, 'dispatch')
class ProductoListView(ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = "nucleo/aaa.html"
    context_object_name = 'productos'
    
    # permiso necesario
    permission_required = 'nucleo.producto.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los productos.'

    # Sobrescribir get_queryset para personalizar la lista de productos
    def get_queryset(self):
        return Producto.objects.all()  # Obtener todos los productos

    def get_form_kwargs(self):
        # Agregamos rama para un manejo más rápido de las asociaciones.
        kwargs = super().get_form_kwargs()
        if 'rama' in self.request.GET:
            kwargs['rama'] = self.request.GET.get('rama')
        return kwargs



# Crear un producto
@method_decorator(login_required, 'dispatch')
class ProductoCreateView(ValidatePermissionRequiredMixin, CreateView):
    # OPCIONES
    template_name = "nucleo/producto-crearv2.html"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('administrador:producto:lista')

    # permiso necesario
    permission_required = 'nucleo.producto.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:producto:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un productos.'

    def get_form_kwargs(self):
        # agregamos rama para un manejo más rapido de las asociaciones.
        kwargs = super().get_form_kwargs()
        if 'rama' in self.request.GET:
            kwargs['rama'] = self.request.GET.get('rama')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pautas'] = Pauta.objects.all()
        return context

    def form_valid(self, form):
        # obtenemos el producto a partir del formulario
        self.object = form.save()
        descriptores = self.request.POST.getlist('descriptores[]')
        descriptores_c = self.request.POST.getlist('descriptores_c[]')
        descriptores_consumo = self.request.POST.getlist('descriptores_consumo[]')
        descriptores_d = self.request.POST.getlist('descriptores_d[]')
        insumos = [int(x) for x in self.request.POST.getlist('insumoe[]')]
        insumos_c = [float(x) for x in self.request.POST.getlist('insumoe_c[]')]
        for i, insumo in enumerate(insumos):
            existe = Insumo.objects.filter(pk=insumo).first()
            if existe:
                self.object.insumoelaboracionproducto_set.create(insumo=existe,cantidad=insumos_c[i])
        listaf = []
        for i in range(len(descriptores)):
            insumo = {'producto_id': self.object.id, 'insumo_id': descriptores[i:i+1][0], 'porcentaje_uso': descriptores_consumo[i:i+1][0], 'cantidad': descriptores_c[i:i+1][0], 'detalle': descriptores_d[i:i+1][0]}
            if insumo['insumo_id'] not in listaf:
                listaf.append(insumo['insumo_id'])
                insumo = InsumoDirectoProducto(**insumo)
                insumo.save()
                self.object.descriptores.add(insumo.insumo)
        self.object.save()
        # obtenemos las pautas
        pautapip = self.request.POST.get('pauta_pip', None)
        pautalinea = self.request.POST.get('pauta_linea', None)
        if pautapip != '' and pautapip is not None:
            self.object.pautapip_id = int(pautapip)
        if pautalinea != '' and pautalinea is not None:
            self.object.pautalinea_id = int(pautalinea)
            pautal = Pauta.objects.filter(pk=int(pautalinea)).first()
            if pautal is not None:
                producto = pautal.pautaproducto_set.filter(producto__pk=self.object.pk).first()
                if producto is None:
                    pautal.pautaproducto_set.create(producto_id=self.object.pk)
        self.object.save()
        historial_crear_producto(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())



@method_decorator(login_required, 'dispatch')
class ProductoDetailView(ValidatePermissionRequiredMixin, View):
    model = Producto
    template_name = 'nucleo/producto_detalle.html'

    def get(self, request, *args, **kwargs):
        # Obtener el producto a partir del PK
        producto = get_object_or_404(self.model, pk=kwargs.get('pk'))

        # Filtrar los datos de los modelos relacionados por el producto
        insumos_elaboracion = InsumoElaboracionProducto.objects.filter(producto=producto)
        insumos_directos = InsumoDirectoProducto.objects.filter(producto=producto)

      
        context = {
            'producto': producto,
            'insumos_elaboracion': insumos_elaboracion,
            'insumos_directos': insumos_directos,  # Pasamos los insumos con el costo total calculado
        }

        # Renderizar la plantilla con el contexto
        return render(request, self.template_name, context)

# Actualizar un producto
@method_decorator(login_required, 'dispatch')
class ProductoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # OPCIONES
    template_name = "nucleo/producto-actualizar.html"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('administrador:producto:lista')

    # permiso necesario
    permission_required = 'nucleo.producto.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:producto:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar el producto.'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pautas'] = Pauta.objects.all()
        return context

    def form_valid(self, form):
        # obtenemos el producto a partir del formulario
        self.object = form.save()
        if self.request.POST.get('actualizar', "") != "":
            self.object.codigo = self.object.generarCodigo()
        descriptores = self.request.POST.getlist('descriptores[]')
        descriptores_c = self.request.POST.getlist('descriptores_c[]')
        descriptores_consumo = self.request.POST.getlist('descriptores_consumo[]')
        descriptores_d = self.request.POST.getlist('descriptores_d[]')
        insumos = [int(x) for x in self.request.POST.getlist('insumoe[]')]
        insumos_c = [float(x) for x in self.request.POST.getlist('insumoe_c[]')]
        listaf = []
        self.object.descriptores.clear()
        
        for i in range(len(descriptores)):
            insumo = {'producto_id': self.object.id, 'insumo_id': descriptores[i:i+1][0], 'porcentaje_uso': descriptores_consumo[i:i+1][0], 'cantidad': descriptores_c[i:i+1][0], 'detalle': descriptores_d[i:i+1][0]}
            if insumo['insumo_id'] not in listaf:
                listaf.append(insumo['insumo_id'])
                insumo = InsumoDirectoProducto(**insumo)
                insumo.save()
                self.object.descriptores.add(insumo.insumo)
        for i, insumo in enumerate(insumos):
            # vemos si existe
            existe = self.object.insumoelaboracionproducto_set.filter(insumo_id=insumo).first()
            if existe:
                existe.cantidad = insumos_c[i]
                existe.save()
            else:
                self.object.insumoelaboracionproducto_set.create(insumo_id=insumo,cantidad=insumos_c[i])
        diferencia = [insumo for insumo in self.object.insumoelaboracionproducto_set.all() if insumo.insumo.id not in insumos]
        for d in diferencia:
            d.delete()
        # obtenemos las pautas
        pautapip = self.request.POST.get('pauta_pip', None)
        pautalinea = self.request.POST.get('pauta_linea', None)
        if pautapip != '' and pautapip is not None:
            self.object.pautapip_id = int(pautapip)
        if pautalinea != '' and pautalinea is not None:
            antigua = self.object.pautalinea
            if antigua is not None:
                existe = antigua.pautaproducto_set.filter(producto__pk=self.object.pk).first()
                if existe is not None:
                    existe.delete()
            self.object.pautalinea_id = int(pautalinea)
            pautal = Pauta.objects.filter(pk=int(pautalinea)).first()
            if pautal is not None:
                producto = pautal.pautaproducto_set.filter(producto__pk=self.object.pk).first()
                if producto is None:
                    pautal.pautaproducto_set.create(producto_id=self.object.pk)
        self.object.save()
        historial_actualizar_producto(self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())


# Eliminar un producto
@method_decorator(login_required, 'dispatch')
class ProductodeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'nucleo.producto.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            producto = get_object_or_404(Producto, pk=kwargs.get('pk'))
            historial_eliminar_producto(self.request.user, producto)
            producto.delete()
            return JsonResponse({'estado': 'ok', 'producto': producto.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

# vista protegida para los archivos adjuntos
def protected_media(request):

    user = request.user
    if user.is_authenticated:
        response = HttpResponse()
        response["X-Accel-Charset"] = "utf-8"
        del response['Content-Type']
        if request.path.replace('/media/', '/')[0:7] == '/firmas':
            if user.has_perm('calidad.registrolimpiezaequipo.excel'):
                response['X-Accel-Redirect'] = '/protected/' + request.path.replace('/media/', '/')
                print(request.path)
                return response
            else:
                if user.perfil:
                    print('firma')
                    print(user.perfil.firma_digital.name)
                    if request.path == user.perfil.firma_digital.name:
                        response['X-Accel-Redirect'] = '/protected/' + request.path.replace('/media/', '/')
                        print(request.path)
                        return response
                    else:
                        return HttpResponseForbidden('No tienes acceso para ver este archivo.')
                else:
                    return HttpResponseForbidden('No tienes acceso para ver este archivo.')
        # Content-type will be detected by nginx
        response['X-Accel-Redirect'] = '/protected/' + request.path.replace('/media/', '/')
        print(request.path)
        return response
        return serve(request, path, settings.MEDIA_ROOT)
    else:
        return HttpResponseForbidden('No tienes acceso para ver este archivo.')

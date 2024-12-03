from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
import pandas as pd
from django.conf import settings
from inventario.models import InventarioProducto
from logistica.models import Ruta, RutaOv
from produccion.models import CajaLote, Lote
from django.db.models import Sum
from .tasks import add
from .functions import generar_excel,exportar_excel
from io import BytesIO
import datetime
#pdf
from xhtml2pdf import pisa
import os
from django.template.loader import get_template

import requests

from rest_framework import viewsets, mixins

from clientes.models import Cliente

from .forms import ListaPrecioForm, OrdenDeVentaAsignarForm, OrdenDeVentaCargarForm, OrdenDeVentaExcelForm, OrdenDeVentaFacturarForm, OrdenDeVentaForm, OrdenDeVentaPickearForm, OrdenDeVentaPickearOVForm, OrdenDeVentaReAsignarForm, OrdenDeVentaUpdateForm
from .serializers import ListaPrecioSerializer, OrdenDeVentaSerializer
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.http.response import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from .models import ArchivoOrdenDeVenta, ListaPrecio, OrdenDeVenta
from rest_framework.generics import RetrieveAPIView
from django.urls import reverse_lazy
from nucleo.models import Producto


# API PARA OBTENER LAS ORDENES PENDIENTES POR CLIENTE
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaPorClienteApiView(ValidatePermissionRequiredMixin, RetrieveAPIView):
    serializer_class = OrdenDeVentaSerializer
    queryset = OrdenDeVenta.objects.all()
    # permiso necesario
    permission_required = 'clientes.cliente.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los clientes.'

    def get_object(self):
        cliente = get_object_or_404(Cliente, pk=self.kwargs.get('cliente'))
        orden = OrdenDeVenta.objects.filter(cliente=cliente, estado='Pendiente').first()
        if orden:
            return orden
        else:
            raise Http404
    
    def get(self, request, *args, **kwargs):
        
        return super().get(request, *args, **kwargs)
    

# API PARA LISTAS DE PRECIOS


@method_decorator(login_required, 'dispatch')
class ListaPrecioViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # permiso necesario para ver la lista de listas de precios
    permission_required = 'ventas.listap.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las listas de precios.'
    # las listas de precio de compras que seran mostradas en la api rest
    queryset = ListaPrecio.objects.all()
    serializer_class = ListaPrecioSerializer

# Listar listas de precios


@method_decorator(login_required, 'dispatch')
class ListaPrecioListView(ValidatePermissionRequiredMixin, TemplateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.listap.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las listas de precios.'
    # template
    template_name = "ventas/lista/list.html"

# agregar lista de precios


@method_decorator(login_required, 'dispatch')
class ListaPrecioCreateView(ValidatePermissionRequiredMixin, CreateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.listap.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear las listas de precios.'
    # template
    template_name = "ventas/lista/create.html"
    form_class = ListaPrecioForm
    success_url = reverse_lazy('ventas:listap:lista')

    # añadimos los productos al contexto
    def get_context_data(self, **kwargs):
        context = super(ListaPrecioCreateView, self).get_context_data(**kwargs)
        # obtenemos los productos
        context['productos'] = Producto.objects.all()
        return context

    # validación del formulario
    def form_valid(self, form):
        # obtenemos el objeto sin guardar
        self.object = form.save(commit=False)
        # obtenemos los productos y sus precios
        identificadores = [int(id) for id in self.request.POST.getlist('identificadores[]')]
        precios = [float(p) for p in self.request.POST.getlist('precios[]')]
        # guardamos los productos y precios procesados en una lista llamada juntos
        juntos = []
        for i in range(len(precios)):
            if precios[i] > 0:
                producto = Producto.objects.filter(pk=identificadores[i]).first()
                if producto is not None:
                    diccionario = {'precio': precios[i], 'producto': producto}
                juntos.append(diccionario)
        # si el tamaño de juntos es mayor a 0, guardamos el objeto con sus productos, si no, mostramos error
        if len(juntos) > 0:
            self.object.save()
            for j in juntos:
                self.object.listaprecioproducto_set.create(producto=j['producto'], precio=j['precio'])
        else:
            form.add_error(None, "Debes agregar al menos un producto a la lista de precios.")
            return super(ListaPrecioCreateView, self).form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

# ACTUALIZAR LISTA DE PRECIOS


@method_decorator(login_required, 'dispatch')
class ListaPrecioUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.listap.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar las listas de precios.'
    # template
    template_name = "ventas/lista/update.html"
    # formulario a utilizar
    form_class = ListaPrecioForm
    # modelo
    model = ListaPrecio
    # url de redireccionamiento
    success_url = reverse_lazy('ventas:listap:lista')

    # añadimos los productos al contexto
    def get_context_data(self, **kwargs):
        context = super(ListaPrecioUpdateView, self).get_context_data(**kwargs)
        # obtenemos los productos
        listaproductos = context['object'].listaprecioproducto_set.all()
        productos = Producto.objects.all()
        # obtenemos el precio del producto actual
        for p in productos:
            if p in [listaproducto.producto for listaproducto in listaproductos]:
                precio = [listaproducto.precio for listaproducto in listaproductos if listaproducto.producto == p][0]
                p.precio = str(precio).replace(',', '.')
                locacion = p.precio.find('.')
                p.precio = p.precio[0:locacion+3]
            else:
                p.precio = 0
        context['productos'] = productos
        return context

    # validación del formulario
    def form_valid(self, form):
        # obtenemos el objeto sin guardar
        self.object = form.save(commit=False)
        # obtenemos el cliente y el checked
        cliente = self.request.POST.get('cliente')
        nueva = self.request.POST.get('nueva')
        nombre = form.data.get('nombre',None)
        if nueva is not None:
            # vemos si ya existe una lista de precios con el nombre seleccionado
            listap = ListaPrecio.objects.filter(nombre=nombre).first()
            if listap is not None:
                form.add_error('nombre', "El nombre ya se encuentra en uso")
                return super(ListaPrecioUpdateView, self).form_invalid(form)
        # obtenemos los productos y sus precios
        identificadores = [int(id) for id in self.request.POST.getlist('identificadores[]')]
        precios = [float(p) for p in self.request.POST.getlist('precios[]')]
        # guardamos los productos y precios procesados en una lista llamada juntos
        juntos = []
        productos = 0
        for i in range(len(precios)):
            if precios[i] > 0:
                productos += 1
            producto = Producto.objects.filter(pk=identificadores[i]).first()
            if producto is not None:
                diccionario = {'precio': precios[i], 'producto': producto}
            juntos.append(diccionario)
        # si no hay precios sobre 0, lanzamos error
        if productos <= 0:
            form.add_error(None, "Debes agregar al menos un producto a la lista de precios.")
            return super(ListaPrecioUpdateView, self).form_invalid(form)
        # guardamos la actualización
        if nueva is None:
            self.object.save()
        else:
            self.object = ListaPrecio.objects.create(nombre=nombre)
        # actualizamos los precios
        for j in juntos:
            # ver si ya existe la relacion
            listap = j['producto'].listaproductos.filter(lista=self.object).first()
            # si existe la relación modificamos el precio
            if listap:
                if j['precio'] <= 0:
                    listap.delete()
                else:
                    listap.precio = j['precio']
                    listap.save()
            else:
                if nueva is not None:
                    if j['precio'] > 0:
                        self.object.listaprecioproducto_set.create(producto=j['producto'], precio=j['precio'])
                else:
                    if j['precio'] > 0:
                        self.object.listaprecioproducto_set.create(producto=j['producto'], precio=j['precio'])
        if cliente != '0':
            try:
                cliente = int(cliente)
                cliente = Cliente.objects.filter(pk=cliente).first()
                if cliente:
                    cliente.listap = self.object
                    cliente.save()
            except Exception as ex:
                print("Error en actualizar lista de precios")
                print(ex)
        return HttpResponseRedirect(self.get_success_url())

# ELIMINAR LISTAS DE PRECIOS


@method_decorator(login_required, 'dispatch')
class ListaPrecioDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'ventas.listap.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            lp = get_object_or_404(ListaPrecio, pk=kwargs.get('pk'))
            # historial_eliminar_lote(self.request.user,estado)
            lp.delete()
            return JsonResponse({'estado': 'ok', 'lp': lp.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

@method_decorator(login_required, 'dispatch')
class ListaPrecioFixView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'ventas.listap.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        listas = ListaPrecio.objects.all()
        for lista in listas:
            for p in lista.listaprecioproducto_set.all():
                p.precio = round(p.precio,2)
                p.save()
        return JsonResponse({'estado': 'ok'})


# ORDENES DE VENTA

# API DE ORDEN DE VENTA
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # permiso necesario para ver la lista de ordenes de venta
    permission_required = 'ventas.orden.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las ordenes de venta.'
    # la lista de ordenes de venta que seran mostradas en la api rest
    queryset = OrdenDeVenta.objects.all()
    serializer_class = OrdenDeVentaSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return OrdenDeVenta.objects.filter()
        else:
            return OrdenDeVenta.objects.filter()

# LISTAR LAS ORDENES DE VENTA


@method_decorator(login_required, 'dispatch')
class OrdenDeVentaListView(ValidatePermissionRequiredMixin, TemplateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las ordenes de venta.'
    # template
    template_name = "ventas/orden/list.html"

@method_decorator(login_required, 'dispatch')
class OrdenDeVentaUploadView(ValidatePermissionRequiredMixin, FormView):
    # permiso necesario para cargar una orden de compra desde un excel
    permission_required = 'ventas.orden.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una orden de venta.'
    # template
    template_name = 'ventas/orden/upload.html'
    form_class = OrdenDeVentaCargarForm
    # url de redireccionamiento
    success_url = reverse_lazy('ventas:orden:lista')

    def form_valid(self, form):
        #check si es archivo o es jumpseller
        codigo_jump = self.request.POST.get('jump', None)
        
        if len(self.request.FILES) != 0:
            file = self.request.FILES['archivo']
            df = pd.read_excel(file)
            encabezado = df.columns[0:3].tolist()
            unimarc = ['Número de Orden', 'Total Neto', 'Forma de Pago']
            jumbo = ['Número de Orden', 'Estado de Orden', 'RUT Comprador']
            lider = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2']
            if unimarc == encabezado:
                # creamos el dataframe de unimarc
                n_orden = df['Número de Orden'][0]
                ean13 = df['Cód. Empaque(EAN13/DUN14)']
                codigo_cliente = df['Cod. PLU SAP']
                desc = df['Descripción Producto']
                unidades = df['Unidades Solicitadas']
                empaque = df['Descripción Empaque']
                unidadexempaque = df['Unidades por Empaque']
                precio = df['Precio Lista Empaque']
                data = ean13, codigo_cliente, desc, unidades, empaque, unidadexempaque, precio
                headers = ['ean13', 'codigo_cliente', 'desc', 'unidades', 'empaque', 'unidadesxempaque', 'precio']
                unimarc = pd.concat(data, axis=1, keys=headers)
                # obtenemos el cliente
                cliente = Cliente.objects.filter(nombre="Unimarc").first()
                if cliente:
                    # obtenemos los locales
                    local_destino = df['Nombre Local Entrega'][0].capitalize()
                    direccion = df['Dirección Local Entrega'][0].capitalize()
                    locales = cliente.clientelocal_set.all()
                    local = None
                    for l in locales:
                        if l.local.lower() == local_destino.lower():
                            local = l
                    # creamos el local
                    if local is None:
                        local = cliente.clientelocal_set.create(local=local_destino.lower(), direccion=direccion, region=cliente.region, comuna=cliente.comuna)
                    # obtenemos la lista de precios
                    listap = cliente.listap
                    if listap:
                        productos = listap.listaprecioproducto_set.all()
                        # Creamos la Orden de Venta
                        ov = OrdenDeVenta.objects.create(local=local, lugar=self.request.user.perfil.lugar, cliente=cliente, fecha=datetime.datetime.now(), n_orden_cliente=n_orden)
                        for index, row in unimarc.iterrows():
                            ean13 = str(row['ean13']).strip()
                            for p in productos:
                                if p.producto.dun14 == '17804632980026':
                                    continue
                                if ((ean13 == p.producto.dun14) or (ean13 == p.producto.ean13())):
                                    precio = row['precio']
                                    if row['empaque'] == 'Caja':
                                        unidades = row['unidades'] * row['unidadesxempaque']
                                    else:
                                        unidades = row['unidades']
                                    ov.ordendeventaproducto_set.create(producto=p.producto, cantidad=unidades, precio=p.precio, codigo_cliente=str(row['codigo_cliente']))
                        return HttpResponseRedirect(reverse_lazy('ventas:orden:actualizar', kwargs={'pk':ov.pk}))
                    else:
                        print("El cliente no posee una lista de precios")
                        raise Http404
        
            if jumbo == encabezado:
                encabezado = df.columns[0:3].tolist()
                ean13 = df['EAN13']
                n_orden = df['Número de Orden'][0]
                codigo_cliente = df['Cód. Cencosud']
                empaque = df['Empaques Pedidos']
                unidadexempaque = df['Unidades por Empaque']
                precio = df['Precio Lista Empaque']
                data = ean13, codigo_cliente, empaque, unidadexempaque, precio
                headers = ['ean13', 'codigo_cliente', 'empaque', 'unidadesxempaque', 'precio']
                jumbo = pd.concat(data, axis=1, keys=headers)
                # obtenemos el cliente
                cliente = Cliente.objects.filter(nombre="Jumbo").first()
                if cliente:
                    # obtenemos los locales
                    local_destino = df['Local Destino'][0].capitalize()
                    direccion = df['Dirección Local Destino'][0].capitalize()
                    locales = cliente.clientelocal_set.all()
                    local = None
                    for l in locales:
                        if l.local.lower() == local_destino.lower():
                            local = l
                    # creamos el local
                    if local is None:
                        local = cliente.clientelocal_set.create(local=local_destino.lower(), direccion=direccion, region=cliente.region, comuna=cliente.comuna)
                    # obtenemos la lista de precios
                    listap = cliente.listap
                    if listap:
                        productos = listap.listaprecioproducto_set.all()
                        # Creamos la Orden de Venta
                        ov = OrdenDeVenta.objects.create(local=local, lugar=self.request.user.perfil.lugar, cliente=cliente, fecha=datetime.datetime.now(), n_orden_cliente=n_orden)
                        for index, row in jumbo.iterrows():
                            ean13 = str(row['ean13']).strip()
                            for p in productos:
                                if p.producto.dun14 == '17804632980026':
                                    continue
                                if ((ean13 == p.producto.dun14) or (ean13 == p.producto.ean13())):
                                    precio = row['precio']
                                    unidades = row['unidadesxempaque'] * row['empaque']
                                    ov.ordendeventaproducto_set.create(producto=p.producto, cantidad=unidades, precio=p.precio, codigo_cliente=str(row['codigo_cliente']))
                        return HttpResponseRedirect(reverse_lazy('ventas:orden:actualizar', kwargs={'pk': ov.pk}))

            if lider == encabezado:
                productos = df[16:-1].copy()
                columnas = ['Linea', 'Codigo UPC', 'ITEM', 'Cod. Prov.', 'Talla/UM', 'Color/Desc', 'Cantidad', 'Precio', 'UEmpaque', 'Empaques', 'Importe']
                productos.set_axis(columnas, axis=1, inplace=True)
                productosf = []
                producto = {'linea': '', 'codigo UPC': '', 'ITEM': '', 'Cod. Prov': '', 'Talla/UM': '', 'Color/Desc': '', 'Cantidad': '', 'Precio': '', 'UEmpaque': '', 'Empaques': '', 'Importe': ''}
                for index, row in productos.iterrows():
                    check = row.isnull().sum()
                    if check == 0:
                        producto['linea'] = row['Linea']
                        producto['codigo UPC'] = row['Codigo UPC']
                        producto['ITEM'] = row['ITEM']
                        producto['Cod. Prov'] = row['Cod. Prov.']
                        producto['Talla/UM'] = row['Talla/UM']
                        producto['Color/Desc'] = row['Color/Desc']
                        producto['Cantidad'] = row['Cantidad']
                        producto['Precio'] = row['Precio']
                        producto['UEmpaque'] = row['UEmpaque']
                        producto['Empaques'] = row['Empaques']
                        producto['Importe'] = row['Importe']
                    if check == 11:
                        if producto['linea'] != '':
                            productosf.append(producto)
                        producto = {'linea': '', 'codigo UPC': '', 'ITEM': '', 'Cod. Prov': '', 'Talla/UM': '', 'Color/Desc': '', 'Cantidad': '', 'Precio': '', 'UEmpaque': '', 'Empaques': '', 'Importe': ''}
                n_orden = df.iloc[2, 1].split('(')[0]
                direccion = df.iloc[5, 3].split('- ')[1]
                local = df.iloc[9, 1]
                localn = local.split(' ')[0]
                direccion = direccion.split(localn + " ")[1]
                # obtenemos el cliente
                cliente = Cliente.objects.filter(nombre="Walmart").first()
                if cliente:
                    # obtenemos los locales
                    local_destino = local
                    locales = cliente.clientelocal_set.all()
                    local = None
                    for l in locales:
                        if l.local.lower() == local_destino.lower():
                            local = l
                            break
                    # creamos el local
                    if local is None:
                        local = cliente.clientelocal_set.create(local=local_destino.lower(), direccion=direccion, region=cliente.region, comuna=cliente.comuna)
                    # obtenemos la lista de precios
                    listap = cliente.listap
                    if listap:
                        productos = listap.listaprecioproducto_set.all()
                        # Creamos la Orden de Venta
                        ov = OrdenDeVenta.objects.create(local=local, lugar=self.request.user.perfil.lugar, cliente=cliente, fecha=datetime.datetime.now(), n_orden_cliente=n_orden)
                        for producto in productosf:
                            ean13 = str(producto['codigo UPC'])
                            for p in productos:
                                if p.producto.dun14 == '17804632980026':
                                    continue
                                if ((ean13 == p.producto.dun14) or (ean13 == p.producto.ean13())):
                                    precio = p.precio
                                    unidades = producto['UEmpaque'] * producto['Empaques']
                                    ov.ordendeventaproducto_set.create(producto=p.producto, cantidad=unidades, precio=p.precio, codigo_cliente=str(producto['ITEM']))
                        return HttpResponseRedirect(reverse_lazy('ventas:orden:actualizar', kwargs={'pk': ov.pk}))
        
        elif codigo_jump is not None or codigo_jump != '':
            # obtenemos la orden de numero
            login = '?login={}&authtoken={}'.format(settings.JUMP_SELLER_KEYS['login'],settings.JUMP_SELLER_KEYS['auth'])
            endpoint = 'https://api.jumpseller.com/v1/'
            url = endpoint + 'orders/{}.json' + login
            url_producto = endpoint + 'products/{}.json' + login
            o = requests.get(url.format(codigo_jump))
            if o.status_code != 200:
                form.add_error(None, "El Código de Orden de Jump Seller es invalido.")
                return super(OrdenDeVentaUploadView, self).form_invalid(form)
            orden = o.json()['order']
            antigua = OrdenDeVenta.objects.filter(n_orden_cliente__icontains=orden['id']).first()
            if antigua is not None:
                form.add_error(None, "La orden n° {} ya se encuentra en el sistema.".format(orden['id']))
                return super(OrdenDeVentaUploadView, self).form_invalid(form)
            # obtenemos el cliente
            cliente = Cliente.objects.filter(nombre='Jumpseller').first()
            if cliente:
                shipping = orden['shipping_address']
                costo_envio = orden['shipping']
                customer = orden['customer']
                # obtenemos el local o creamos uno nuevo (dirección del cliente)
                dlocal = {'direccion': shipping['address'], 'local': '{} {} {}'.format(shipping['name'], shipping['surname'], customer['id']), 'region': shipping['region'], 'comuna': shipping['municipality'], 'telefono': customer['phone'], 'contacto': '{} {}'.format(shipping['name'],shipping['surname']), 'email': customer['email']}
                local = cliente.clientelocal_set.filter(local__icontains=customer['id']).first()
                if local is None:
                    # actualizamos el local con la ultima direccion
                    local = cliente.clientelocal_set.create(**dlocal)
                cliente.clientelocal_set.filter(pk=local.pk).update(**dlocal)
                # obtenemos la lista de precios
                listap = cliente.listap
                if listap:
                    productos = listap.listaprecioproducto_set.all()
                    # Creamos la Orden de Venta
                    ov = OrdenDeVenta.objects.create(local=local, lugar=self.request.user.perfil.lugar, cliente=cliente, fecha=datetime.datetime.now(), n_orden_cliente="JUMPSELLER{}".format(orden['id']), envio=costo_envio)
                    for producto in orden['products']:
                        sku = producto['sku']
                        if sku is None:
                            r = requests.get(url_producto.format(producto['id']))
                            p = r.json()['product']
                            sku = p['sku']
                        if sku is None:
                            continue
                        for p in productos:
                            if p.producto.id == int(sku):
                                ov.ordendeventaproducto_set.create(producto=p.producto, cantidad=producto['qty'], precio=p.precio, codigo_cliente=producto['id'])
                    return HttpResponseRedirect(reverse_lazy('ventas:orden:actualizar', kwargs={'pk':ov.pk}))

        

        raise Http404


    # def post

# Orden de venta PDF
# Vista PDF
@method_decorator(login_required, 'dispatch')
class OrdenVentaPdfView(ValidatePermissionRequiredMixin, View):
    # permisos necesarios
    permission_required = 'ventas.orden.crear'

    def link_callback(self, uri, rel):
        # nombres acortados de las variables de settings
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT  
        mUrl = settings.MEDIA_URL  
        mRoot = settings.MEDIA_ROOT

        # Se convierten las uris a rutas aboslutas
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # checkear si el archivo realmente existe
        if not os.path.isfile(path):
            raise Exception(
                'La url de archivos media debe comenzar con %s o %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        # buscamos la orden y si no mostramos error 404
        orden = get_object_or_404(OrdenDeVenta, pk=self.kwargs['pk'])
        # definimos la template que utilizaremos
        template_path = 'ventas/orden/pdf.html'
        # el contexto que sera utilizado en la plantilla de django
        context = {'orden': orden, 'logo': '{}{}'.format(settings.STATIC_URL, 'nucleo/img/logo.png'), 'empresa': settings.CONFIGURACION_PDF, 'request': request}
        # generamos el pdf y lo transformamos para que sea visible desde el navegador
        response = BytesIO()
        template = get_template(template_path)
        html = template.render(context)
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),response,link_callback=self.link_callback)
        if pdf.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        response = HttpResponse(response.getvalue(),content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename=Nota de venta #{orden.id}.pdf'
        return response

# AGREGAR ORDEN DE VENTA
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaCreateView(ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'ventas.orden.crear'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una orden de venta.'
    template_name = "ventas/orden/create.html"
    form_class = OrdenDeVentaForm
    success_url = reverse_lazy('ventas:orden:lista')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Obtenemos los datos del formulario
        productos = self.request.POST.getlist('idproducto[]')
        cantidades = self.request.POST.getlist('cantidadproducto[]')
        precios = self.request.POST.getlist('precioproducto[]')
        descuentos = self.request.POST.getlist('descuentoproducto[]')
        codigos = self.request.POST.getlist('codigo_cliente[]')

        # Obtenemos el lugar
        local = self.request.POST.get('local')
        cliente = self.object.cliente
        
        # Asignar local
        if local == 'matriz':
            localc = cliente.clientelocal_set.filter(local='Casa Matriz').first()
            if localc is None:
                localc = cliente.clientelocal_set.create(local='Casa Matriz', 
                                                          direccion=cliente.direccion, 
                                                          comuna=cliente.comuna, 
                                                          region=cliente.region, 
                                                          telefono=cliente.telefono, 
                                                          contacto=cliente.contacto)
            self.object.local = localc
        else:
            try:
                local = int(local)
                local = cliente.clientelocal_set.filter(pk=local).first()
                if local:
                    self.object.local = local
            except Exception as ex:
                self.object.local = None
        
        if self.object.local is None:
            form.add_error(None, "Ha ocurrido un problema al asignar el local a la venta, por favor intenta nuevamente")
            return super().form_invalid(form)

        self.object.lugar = self.request.user.perfil.lugar
        self.object.save()

        # Procesar productos
        for i in range(len(cantidades)):
            cantidad = cantidades[i]
            try:
                cantidad = int(cantidad)
            except Exception:
                continue
            
            if cantidad > 0:
                try:
                    producto = Producto.objects.filter(pk=int(productos[i])).first()
                    precio = float(precios[i])
                    descuento = float(descuentos[i])
                    if producto:
                        self.object.ordendeventaproducto_set.create(producto=producto, 
                                                                    cantidad=cantidad, 
                                                                    precio=precio, 
                                                                    descuento=descuento, 
                                                                    codigo_cliente=str(codigos[i]))
                except Exception:
                    continue

        # Guardar archivos
        files = self.request.FILES.getlist('archivos')
        for f in files:
            self.object.archivoordendeventa_set.create(archivo=f)

        self.object.complitud = self.object.calcularComplitud()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# DETALLE OV
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaDetailView(ValidatePermissionRequiredMixin, DetailView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una orden de venta.'
    # template
    template_name = "ventas/orden/detail.html"
    model = OrdenDeVenta

# Actualizar Orden de Venta
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una orden de venta.'
    # template
    template_name = "ventas/orden/update.html"
    form_class = OrdenDeVentaUpdateForm
    success_url = reverse_lazy('ventas:orden:lista')
    model = OrdenDeVenta

    def form_valid(self, form):
        self.object = form.save()
        productos = self.request.POST.getlist('idproducto[]')
        cantidades = self.request.POST.getlist('cantidadproducto[]')
        precios = self.request.POST.getlist('precioproducto[]')
        descuentos = self.request.POST.getlist('descuentoproducto[]')
        codigos = self.request.POST.getlist('codigo_cliente[]')
        detalles = self.request.POST.getlist('detalleproducto[]')
        # armamos la lista de productos finales
        for i in range(len(cantidades)):
            # transformamos la cantidad a un entero
            cantidad = cantidades[i]
            try:
                cantidad = int(cantidad)
            except Exception as ex:
                print(ex)
                continue
            # verificamos que sea mayor a 0
            if cantidad > 0:
                # verificamos que el producto exista
                try:
                    producto = Producto.objects.filter(pk=int(productos[i])).first()
                    precio = float(precios[i])
                    descuento = float(descuentos[i])
                    # vemos si existe ya el producto en los productos de la orden de venta
                    if producto:
                        ovp = self.object.ordendeventaproducto_set.filter(producto=producto).first()
                        if ovp is not None:
                            ovp.cantidad = cantidad
                            ovp.precio = precio
                            ovp.descuento = descuento
                            ovp.codigo_cliente = codigos[i]
                            ovp.save()
                        else:
                            objeto = self.object.ordendeventaproducto_set.create(producto=producto, cantidad=cantidad, precio=precio,descuento=descuento, codigo_cliente=codigos[i])
                except Exception as ex:
                    continue
            else:
                try:
                    producto = Producto.objects.filter(pk=int(productos[i])).first()
                    if producto:
                        ovp = self.object.ordendeventaproducto_set.filter(producto=producto).first()
                        if ovp:
                            ovp.delete()
                except Exception as ex:
                    print(ex)
                    continue
        # guardamos los archivos
        files = self.request.FILES.getlist('archivos')
        for f in files:
            self.object.archivoordendeventa_set.create(archivo=f)
        return HttpResponseRedirect(self.get_success_url())


# Imprimir Orden de Venta
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaExcel(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'ventas.orden.listar'
    url_redirect = reverse_lazy('ventas:orden:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para imprimir la ov.'
    model = OrdenDeVenta

    def dispatch(self, request, *args, **kwargs):
        ov = OrdenDeVenta.objects.filter(pk=int(kwargs.get('pk'))).first()
        if ov is None:
            raise Http404
        else:
            excel = generar_excel(ov, self.request)
            stream = BytesIO()
            excel.save(stream)

            response = HttpResponse(stream.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename={}'.format('ov{}.xlsx'.format(ov.pk))
            return response

# Pickear OV por codigo de ov
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaPickearView(ValidatePermissionRequiredMixin, UpdateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.pickear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para pickear una orden de venta.'
    # template
    template_name = "ventas/orden/pickearov.html"
    form_class = OrdenDeVentaPickearOVForm
    success_url = reverse_lazy('ventas:orden:lista')
    model = OrdenDeVenta

    def dispatch(self, request, *args, **kwargs):
        ov = super().get_object()
        if ov.estado != 'Pendiente':
            raise Http404('La orden no esta en estado pendiente.')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ov = form.save()
        post = self.request.POST
        if ov:
            cajas = [int(elemento) for elemento in post.getlist('cajas[]')]
            idproducto = [int(elemento) for elemento in post.getlist('idproducto[]')]
            cantidad_caja = [int(elemento) for elemento in post.getlist('cantidadfccaja[]')]
            cantidad_mano = [int(elemento) for elemento in post.getlist('cantidadfc[]')]
            # procesar las cajas y dejarlas amarradas al pedido
            for caja in cajas:
                cajalote = CajaLote.objects.filter(pk=caja).first()
                if cajalote:
                    cajalote.estado = 'Pickeado'
                    cajalote.save()
                    ov.ordendeventacajalote_set.create(caja=cajalote,cantidad=cajalote.cantidad)
            for i in range(len(idproducto)):
                idp = int(idproducto[i])
                cantidadc = int(cantidad_caja[i])
                cantidadm = int(cantidad_mano[i])
                sumados = cantidadc+cantidadm
                ordenp = ov.ordendeventaproducto_set.filter(producto_id=idp).first()
                if ordenp:
                    if sumados > ordenp.cantidad:
                        form.add_error(None, "No puedes agregar más cantidad de la solicitada en {} ({} {}) solicitaron {} pickeaste {}".format(ordenp.producto.nombre,ordenp.producto.presentacion,ordenp.producto.unidad,ordenp.cantidad,sumados))
                        return super(OrdenDeVentaPickearView, self).form_invalid(form)
                    if cantidadm > 0:
                        cantidada = cantidadm
                        queryset = CajaLote.objects.filter(lote__producto_id=idp, estado='Abierta', lugar=self.request.user.perfil.lugar)
                        if len(queryset) > 0:
                            total = queryset.aggregate(Sum('cantidad'))['cantidad__sum'] - queryset.aggregate(Sum('cantidad_a'))['cantidad_a__sum']
                        else:
                            total = 0
                        if settings.SALTARPICKEO:
                            total = 999999999
                        if cantidadm > total:
                            form.add_error(None, "No puedes completar esta orden debido a que en el inventario de cajas abiertas de {} ({} {}) solamente hay {} unidades y necesitas {}".format(ordenp.producto.nombre,ordenp.producto.presentacion,ordenp.producto.unidad,total,ordenp.cantidad))
                            return super(OrdenDeVentaPickearView, self).form_invalid(form)
                        for cajaa in queryset.all():
                            if cantidada > 0:
                                totald = cajaa.cantidad - cajaa.cantidad_a
                                if cantidada >= totald:
                                    cajaa.cantidad_a = cajaa.cantidad
                                    cantidada -= totald
                                    ov.ordendeventacajalote_set.create(caja=cajaa,cerrada=False,cantidad=totald)
                                    cajaa.save()
                                else:
                                    resta = totald - cantidada
                                    cajaa.cantidad_a = cajaa.cantidad - resta
                                    cantidada = 0
                                    ov.ordendeventacajalote_set.create(caja=cajaa,cerrada=False,cantidad=cajaa.cantidad_a)
                                    cajaa.save()

                    ordenp.cantidad_fc = sumados
                    ordenp.save()
                    ip, created = InventarioProducto.objects.get_or_create(producto_id=idp, bodega=ov.lugar, defaults={'cantidad': 0})
                    ip.cantidad -= ordenp.cantidad_fc
                    ip.save()
            ov.estado = 'Pickeado'
            ov.save()
        return HttpResponseRedirect(self.get_success_url())

# Pickear Orden de venta
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaPickView(ValidatePermissionRequiredMixin, FormView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.pickear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para pickear una orden de venta.'
    # template
    template_name = "ventas/orden/pickear.html"
    form_class = OrdenDeVentaPickearForm
    success_url = reverse_lazy('ventas:orden:lista')

    def form_valid(self, form):
        post = self.request.POST
        ov = OrdenDeVenta.objects.filter(cliente_id=int(post.get('cliente')), pk=int(post.get('ov'))).first()
        if ov:
            cajas = [int(elemento) for elemento in post.getlist('cajas[]')]
            idproducto = [int(elemento) for elemento in post.getlist('idproducto[]')]
            cantidad_fc = [int(elemento) for elemento in post.getlist('cantidadfc[]')]
            # procesar las cajas y dejarlas amarradas al pedido
            for caja in cajas:
                cajalote = CajaLote.objects.filter(pk=caja).first()
                if cajalote:
                    cajalote.estado = 'Pickeado'
                    cajalote.save()
                    ov.ordendeventacajalote_set.create(caja=cajalote)
            for i in range(len(idproducto)):
                idp = int(idproducto[i])
                cantidad = int(cantidad_fc[i])
                ordenp = ov.ordendeventaproducto_set.filter(producto_id=idp).first()
                if ordenp:
                    if cantidad > ordenp.cantidad:
                        form.add_error(None, "No puedes agregar más cantidad de la solicitada en {} ({} {}) solicitaron {} pickeaste {}".format(ordenp.producto.nombre,ordenp.producto.presentacion,ordenp.producto.unidad,ordenp.cantidad,cantidad))
                        return super(OrdenDeVentaPickView, self).form_invalid(form)
                    ordenp.cantidad_fc = cantidad
                    ordenp.save()
                    ip,created = InventarioProducto.objects.get_or_create(producto_id=idp,bodega=ov.lugar,defaults={'cantidad':0})
                    ip.cantidad -= ordenp.cantidad_fc
                    ip.save()
            ov.estado = 'Pickeado'
            ov.save()
        return HttpResponseRedirect(self.get_success_url())

# FACTURAR ORDEN DE VENTA
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaFacturaView(ValidatePermissionRequiredMixin, UpdateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una orden de venta.'
    # template
    template_name = "ventas/orden/facturar.html"
    form_class = OrdenDeVentaFacturarForm
    success_url = reverse_lazy('ventas:orden:lista')
    model = OrdenDeVenta



    def dispatch(self, request, *args, **kwargs):
        ov = super().get_object()
        if ov.estado != 'Pickeado':
            raise Http404('La orden no esta en estado de pickeado.')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        post = self.request.POST
        boleta = post.get('factura')
        idproducto = [int(elemento) for elemento in post.getlist('idproducto[]')]
        factura = [elemento for elemento in post.getlist('factura[]')]
        for i in range(len(idproducto)):
            ovp = self.object.ordendeventaproducto_set.filter(producto_id=idproducto[i]).first()
            if ovp:
                ovp.factura = factura[i].strip()
                ovp.save()
        if boleta is None:
            self.object.estado = 'Boleteado'
        else:
            self.object.estado = 'Facturado'
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# REASIGNAR ORDEN DE VENTA
@method_decorator(login_required,'dispatch')
class OrdenDeVentaReAsignarView(ValidatePermissionRequiredMixin,UpdateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una orden de venta.'
    model = OrdenDeVenta
    form_class = OrdenDeVentaReAsignarForm
    template_name = "ventas/orden/facturar.html"

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.url_redirect)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.estado != 'No Entregado':
            return JsonResponse({'estado': 'error', 'mensaje': 'La orden de venta debe estar no entregada para ser reasignada.'})
        post = self.request.POST
        ruta = Ruta.objects.filter(pk=int(post.get('ruta'))).first()
        if ruta:
            self.object.rutaov_set.all().delete()
            self.object.rutaov_set.create(ruta=ruta)
            self.object.estado = 'Asignado'
            self.object.save()
        return JsonResponse({'estado': 'ok', 'mensaje': 'La orden #{} ha sido asignada a la ruta {}'.format(self.object.id, ruta.nombre)})


# ASIGNAR ORDEN DE VENTA A RUTA
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaAsignarView(ValidatePermissionRequiredMixin, UpdateView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ventas.orden.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una orden de venta.'
    # template
    template_name = "ventas/orden/asignar.html"
    form_class = OrdenDeVentaAsignarForm
    success_url = reverse_lazy('ventas:orden:lista')
    model = OrdenDeVenta

    def dispatch(self, request, *args, **kwargs):
        ov = super().get_object()
        if ov.estado not in ['Facturado', 'Boleteado']:
            raise Http404('La orden no esta en estado facturado.')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        post = self.request.POST
        try:
            ruta = int(post.get('ruta'))
            ruta = get_object_or_404(Ruta, pk=ruta)
            self.object.estado = 'Asignado'
            rutaov = RutaOv.objects.filter(orden=self.object, ruta=ruta).first()
            if rutaov is None:
                rutaov = RutaOv.objects.create(orden=self.object, ruta=ruta)
            # obtenemos las cajas que estan en la ov
            cajas = self.object.ordendeventacajalote_set.all()
            for c in cajas:
                c.caja.estado = 'En Ruta'
                c.caja.save()
            self.object.save()
        except Exception as ex:
            print(ex)
        return HttpResponseRedirect(self.get_success_url())




# ELIMINAR ORDEN DE VENTA
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'ventas.orden.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            ov = get_object_or_404(OrdenDeVenta, pk=kwargs.get('pk'))
            if ov.estado == 'Pendiente':
                # historial_eliminar_lote(self.request.user,estado)
                ov.delete()
                return JsonResponse({'estado': 'ok', 'ov': ov.id})
            return JsonResponse({'estado':'fallo'});
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'});

@method_decorator(login_required, 'dispatch')
class OrdenDeVentaEntregarView(ValidatePermissionRequiredMixin, FormView):
    # permiso
    permission_required = 'ventas.orden.entregar'

    def post(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            if 'estado' in kwargs:
                ov = get_object_or_404(OrdenDeVenta, pk=kwargs.get('pk'))
                estados = ['Entregado', 'Recepción Parcial', 'No Entregado']
                cantidades = self.request.POST.getlist('cantidad_e[]')
                if ov.estado not in estados and ov.estado == 'Asignado':
                    try:
                        productos = [ov.ordendeventaproducto_set.filter(pk=int(id)).first() for id in self.request.POST.getlist('productos[]')]
                        for i in range(len(productos)):
                            productos[i].cantidad_en = productos[i].cantidad_fc - int(cantidades[i])
                            productos[i].save()
                        ov.estado = 'Recepción Parcial'
                        ov.save()
                    except Exception as ex:
                        print(ex)
                return JsonResponse({'estado': 'ok', 'ov': ov.id})
        return JsonResponse({'estado': 'error', 'mensaje': 'Problemas...'})

    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            if 'estado' in kwargs:
                # obtenemos la orden de venta
                ov = get_object_or_404(OrdenDeVenta, pk=kwargs.get('pk'))
                estados = ['Entregado', 'Recepción Parcial', 'No Entregado']
                if ov.estado not in estados:
                    estado = kwargs.get('estado')
                    if estado not in estados:
                        return JsonResponse({'estado': 'fallo'})
                    ov.estado = estado
                    ov.entregado = self.request.user
                    ov.fecha_e = datetime.datetime.now()
                    ov.save()
                    if estado == 'Entregado':
                        # obtenemos las cajas enviadas
                        cajas = ov.ordendeventacajalote_set.all()
                        for c in cajas:
                            c.caja.estado = 'Cliente'
                            c.caja.save()
                    # historial_eliminar_lote(self.request.user,estado)
                    return JsonResponse({'estado': 'ok', 'ov': ov.id})
                else:
                    estado = kwargs.get('estado')
                    if estado == 'Retroceder':
                        if ov.estado == 'Entregado':
                            productos = ov.ordendeventaproducto_set.all()
                            for p in productos:
                                p.cantidad_en = p.cantidad_fc
                                p.save()
                            cajas = ov.ordendeventacajalote_set.all()
                            for c in cajas:
                                c.caja.estado = 'Pickeado'
                                c.caja.save()
                        ov.estado = 'Asignado'
                        ov.entregado = None
                        ov.fecha_e = None
                        ov.save()
                        return JsonResponse({'estado': 'ok', 'ov': ov.id})
                    return JsonResponse({'estado': 'fallo'})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

# Retroceder Orden de Venta


@method_decorator(login_required, 'dispatch')
class OrdenDeVentaRetrocederView(ValidatePermissionRequiredMixin, DetailView):

    # permiso
    permission_required = 'ventas.orden.retroceder'
    model = OrdenDeVenta

    def dispatch(self, request, *args, **kwargs):
        ov = super().get_object()
        if ov.estado not in ['Pickeado', 'Boleteado', 'Facturado', 'Asignado']:
            raise Http404('La orden no se puede retroceder')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        ov = super().get_object()
        estado = ov.estado
        if estado == 'Asignado':
            # obtenemos la ruta al cual esta asignado
            rutaov = ov.rutaov_set.first()
            if rutaov:
                rutaov.delete()
            # vemos si posee facturas
            facturas = ov.get_facturas()
            boleta = False
            for f in facturas:
                if settings.IDENTIFICADOR_BOLETA in f:
                    boleta = True
            if boleta:
                ov.estado = 'Boleteado'
            else:
                ov.estado = 'Facturado'
        elif estado in ['Facturado', 'Boleteado']:
            # obtenemos los productos de la orden
            productos = ov.ordendeventaproducto_set.all()
            # cambiamos su cantidad facturada a 0
            for p in productos:
                p.factura = ""
                p.save()
            ov.estado = 'Pickeado'
        elif estado == 'Pickeado':
            productos = ov.ordendeventaproducto_set.all()
            cajas = ov.ordendeventacajalote_set.all()
            for c in cajas:
                if c.cerrada:
                    c.caja.estado = 'Recepcionado'
                    c.caja.save()
                    c.delete()
                else:
                    c.caja.cantidad_a -= c.cantidad
                    c.caja.estado = 'Abierta'
                    c.caja.save()
                    c.delete()
            for p in productos:
                ip = p.producto.inventarioproducto_set.filter(bodega=ov.lugar).first()
                try:
                    ip.cantidad += p.cantidad_fc
                    ip.save()
                except Exception as ex:
                    print(ex)
                p.cantidad_fc = 0
                p.save()
            ov.estado = 'Pendiente'
        ov.save()
        return JsonResponse({'estado': 'ok'})


# ELIMINAR TODAS ORDEN DE VENTA
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaDeleteAllView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'ventas.orden.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        ordenes = OrdenDeVenta.objects.all()
        for ov in ordenes:
            ov.delete()
        return JsonResponse({'estado': 'ok'})

# API ABRIR CAJA
@method_decorator(login_required,'dispatch')
class APIAbrirCaja(ValidatePermissionRequiredMixin,View):
    # permiso
    permission_required = 'ventas.orden.abrir'
    url_redirect = reverse_lazy('ventas:orden:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para abrir esta caja.'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            print(self.request.GET)
            id_caja = self.request.GET.get('caja')
            unidades = self.request.GET.get('cantidad')
            if id_caja is None or unidades is None:
                return JsonResponse({'estado': 'fallo'})
            # obtenemos el lote
            lote = get_object_or_404(Lote, pk=kwargs.get('pk'))
            # obtenemos sus cajas y filtramos por numero de caja
            caja = lote.cajalote_set.filter(caja=id_caja, cantidad=unidades).first()
            if caja.estado == 'Recepcionado':
                caja.estado = 'Abierta'
                caja.save()
            else:
                return JsonResponse({'estado': 'fallo'})
            return JsonResponse({'estado': 'ok', 'caja': caja.pk})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})


# ELIMINAR ARCHIVO ASOCIADO
@method_decorator(login_required, 'dispatch')
class OrdenDeVentaEliminarArchivo(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'ventas.archivo.eliminar'

    # al obtener la peticion get
    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            archivo = get_object_or_404(ArchivoOrdenDeVenta, pk=kwargs.get('pk'))
            archivo.delete()
            return JsonResponse({'estado': 'ok', 'orden_id': archivo.orden.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

#Generar Excel
@method_decorator(login_required,'dispatch')
class OrdenDeVentaGenerarExcel(ValidatePermissionRequiredMixin,FormView):
    #permiso
    permission_required = 'ventas.orden.excel'
    url_redirect = reverse_lazy('ventas:orden:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para exportar los registros.'

    form_class = OrdenDeVentaExcelForm
    template_name = 'ventas/orden/excel.html'

    def form_valid(self, form):
        #obtenemos las fechas para las cuales queremos generar el excel
        fecha_inicio = form.cleaned_data.get('fechainicio')
        fecha_fin = form.cleaned_data.get('fechafin')
        fecha_fin_m = datetime.datetime(year=fecha_fin.year,month=fecha_fin.month,day=fecha_fin.day).replace(hour = 23,minute=59)
        ov = OrdenDeVenta.objects.filter(fecha__range=[fecha_inicio,fecha_fin_m])
        excel = exportar_excel(fecha_inicio,fecha_fin,ov,self.request)
        stream = BytesIO()
        excel.save(stream)
        response = HttpResponse(stream.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={}'.format('ov-{}.xlsx'.format(fecha_inicio))
        return response

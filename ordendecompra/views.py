from inventario.forms import InsumoBultoUpdateForm
from proveedores.models import ProveedorInsumo
from django.views.generic.base import RedirectView
from django.http.response import Http404, HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView,CreateView,DetailView,View,UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.urls import reverse_lazy,reverse
from .models import OrdenDeCompra,OrdenDeCompraInsumo, Registro, Archivo
from inventario.models import InventarioInsumo, InsumoBulto
from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView
from .serializers import HistorialInsumoSerializer, OrdenDeCompraSerializer
from .forms import OrdenDeCompraCreateForm, OrdenDeCompraEtiquetarForm, OrdenDeCompraValidarForm, OrdenDeCompraRecepcionarForm, OrdenDeCompraPagarForm
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from django import template
import os
from io import BytesIO
from django.http import JsonResponse
from .functions import generar_etiqueta, historial_rechazar_oc,historial_crear_oc,historial_cambiar_estado_oc, historial_eliminar_oc, registrarCambioEstado, historial_eliminara_oc
#codigo de barra
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image, ImageFont, ImageDraw

# funciones auxiliares
def verificarCantidad(x):
    if x == '':
        return '0'
    else:
        return x

# Create your views here.

#API DE PRUEBA
@method_decorator(login_required,'dispatch')
class InsumoListViewApi(ValidatePermissionRequiredMixin,ListAPIView):
    serializer_class = HistorialInsumoSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return OrdenDeCompraInsumo.objects.filter(insumo=int(pk))

#API DE LAS ORDENES DE COMPRA CON LA POSIBILIDAD DE LISTAR Y OBTENER DETALLE
@method_decorator(login_required,'dispatch')
class OrdenDeCompraViewset(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ordendecompra.listar'
    #las ordenes de compras que seran mostradas en la api rest
    queryset = OrdenDeCompra.objects.all()
    #la clase serializer que proviene de .serializers
    serializer_class = OrdenDeCompraSerializer

#MOSTRAR TODAS LAS ORDENES DE COMPRA
@method_decorator(login_required,'dispatch')
class OrdenCompraTemplateView(ValidatePermissionRequiredMixin,TemplateView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'ordendecompra.listar'
    #el template que se renderizara
    template_name = 'ordendecompra/list.html'

#Detalle Orden
@method_decorator(login_required,'dispatch')
class OrdenCompraDetalleView(ValidatePermissionRequiredMixin,DetailView):
    #permisos necesarios
    permission_required = 'ordendecompra.listar'
    #template a utilizar en la vista de detalle
    template_name = 'ordendecompra/detalle.html'
    #modelo de la orden de compra
    model = OrdenDeCompra

    #añadimos información extra al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #registros
        context["registro"] = Registro.objects.filter(orden=self.object)
        #solicita
        context["solicita"] = context["registro"].filter(estado='Inicial').first()
        #archivos
        context["archivos"] = Archivo.objects.filter(orden=self.object)
        return context


@method_decorator(login_required, 'dispatch')
class OrdenCompraDividirBultoView(ValidatePermissionRequiredMixin, UpdateView):
    # permisos necesarios
    permission_required = 'ordendecompra.dividir'
    # template a utilizar en la vista de detalle
    template_name = 'ordendecompra/dividirbulto.html'
    # modelo de la orden de compra
    model = InsumoBulto
    form_class = InsumoBultoUpdateForm

    def get_success_url(self):
        return reverse_lazy('ordendecompra:detalle', kwargs={'pk': self.object.ordendecompra.pk})
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.bodega is None:
            form.add_error(None, "No se puede dividir un bulto si esta en Transito.")
            return super(OrdenCompraDividirBultoView, self).form_invalid(form)
        cantidadbultos = [float(x) for x in self.request.POST.getlist('cantidadbulto')]
        if sum(cantidadbultos) != (self.object.cantidad - self.object.cantidadu):
            form.add_error(None, f"La cantidad ingresada es distinta a la cantidad disponible. {self.object.cantidad - self.object.cantidadu}")
            return super(OrdenCompraDividirBultoView, self).form_invalid(form)
        for c in cantidadbultos:
            if c > 0:
                self.object.padre.create(insumobultohijo=InsumoBulto.objects.create(insumo=self.object.insumo, ordendecompra=self.object.ordendecompra, bodega=self.object.bodega, lotep=self.object.lotep, cantidad=c, cantidadu=0, formato=self.object.formato))
        self.object.cantidadu = self.object.cantidad
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# Vista PDF
@method_decorator(login_required, 'dispatch')
class OrdenCompraPdfView(ValidatePermissionRequiredMixin, View):
    # permisos necesarios
    permission_required = 'ordendecompra.pdf'

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
        orden = get_object_or_404(OrdenDeCompra,pk=self.kwargs['pk'])
        if(orden.estado == 'Inicial'):
            raise Http404
        #obtenemos el valor del dolar y el euro utilizado en esta compra
        dolar = 0
        eur = 0
        insumos = orden.ordendecomprainsumo_set.all()
        for i in insumos:
            if (dolar == 0 or eur == 0):
                if i.insumo.moneda.nombre == 'USD':
                    dolar = i.moneda
                elif i.insumo.moneda.nombre == 'EUR':
                    eur = i.moneda
        # definimos la template que utilizaremos
        template_path = 'ordendecompra/pdf.html'
        # el contexto que sera utilizado en la plantilla de django
        context = {'orden': orden, 'logo': '{}{}'.format(settings.STATIC_URL, 'nucleo/img/logo.png'), 'empresa': settings.CONFIGURACION_PDF, 'request': request, 'dolar': dolar, 'eur': eur}
        # generamos el pdf y lo transformamos para que sea visible desde el navegador
        response = BytesIO()
        template = get_template(template_path)
        html = template.render(context)
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),response,link_callback=self.link_callback)
        if pdf.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        response = HttpResponse(response.getvalue(),content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename=Orden #{orden.numero}.pdf'
        return response

#Vista auxiliar que sirve para redigir al paso de la orden de compra
def paso(request,pk):
    #obtenemos la orden
    orden = get_object_or_404(OrdenDeCompra,pk=pk)
    #diccionario con los posibles estados
    estados = {'inicial': 'ordendecompra:validar', 'validada': 'ordendecompra:recepcionar', 'semi-recepcionada': 'ordendecompra:etiquetar', 'recepcionada': 'ordendecompra:etiquetar', 'etiquetado':'ordendecompra:etiquetar'}
    if orden.estado.lower() in estados:
        #devolvemos el estado correspondiente
        return HttpResponseRedirect(reverse(estados[orden.estado.lower()],args=[orden.id]))
    else:
        #si no hay siguiente paso devolvemos la lista
        return HttpResponseRedirect(reverse('ordendecompra:lista'))


# Crear Orden de Compra
@method_decorator(login_required, 'dispatch')
class OrdenCompraCreateView(ValidatePermissionRequiredMixin, CreateView):
    # Permiso necesario
    permission_required = 'ordendecompra.crear'

    # Obtenemos el número de orden de compra anterior, y le sumamos uno.
    def get_initial(self):
        item = OrdenDeCompra.objects.last()
        if item:
            item = item.numero + 1
        else:
            item = 0
        return {'numero': item, 'estado': 'Inicial'}

    # El modelo que usará nuestra vista de create
    model = OrdenDeCompra
    # La plantilla
    template_name = 'ordendecompra/create.html'
    # El formulario
    form_class = OrdenDeCompraCreateForm
    # La URL donde se redigirá luego de crear la orden de compra
    success_url = reverse_lazy('ordendecompra:lista')

    # Proceso cuando el formulario es válido para agregar los insumos
    def form_valid(self, form):
        # Lista de insumos vacía
        insumos = []
        # Obtenemos las ids de los insumos a agregar
        ids = self.request.POST.getlist('idinsumo[]')
        # Luego su cantidad
        cantidad = self.request.POST.getlist('cantidadinsumo[]')
        # Transformamos los campos vacíos de cantidad a 0
        cantidad = [verificarCantidad(x) for x in cantidad]
        # Sumamos la cantidad de insumos para verificar que al menos haya alguno.
        total = sum([float(x) for x in cantidad])
        # Si el total es menor o igual a 0, devolvemos error.
        if total <= 0:
            return super(OrdenCompraCreateView, self).form_invalid(form)

        # Generamos nuestro objeto orden de compra
        self.object = form.save()
        
        # Obtenemos los detalles y precios
        precioinsumo = self.request.POST.getlist('precioinsumo[]')
        # Generamos nuestros insumos con un diccionario
        for i in range(len(ids)):
            insumo = {
                'orden_id': self.object.id,
                'insumo_id': ids[i],
                'cantidad': cantidad[i],
                'neto': float(precioinsumo[i])
            }
            if int(insumo['cantidad']) > 0:
                insumos.append(insumo)

        # Agregamos nuestros insumos a la orden de compra
        for insumo in insumos:
            o = OrdenDeCompraInsumo(**insumo)
            o.moneda = o.insumo.moneda.valor
            pinsumo = o.insumo
            if pinsumo.moneda.nombre not in ['USD', 'EUR']:
                pinsumo.precio = o.neto
                pinsumo.save()
            o.save()

        # Actualizamos el total neto
        self.object.total_neto = self.object.totalNeto()

        # Guardamos los archivos adjuntos
        archivos = form.cleaned_data.get('archivos')
        if archivos:
            if isinstance(archivos, list):  # Si se permite cargar múltiples archivos
                for f in archivos:
                    Archivo(orden=self.object, archivo=f).save()
            else:  # Si solo se permite un archivo
                Archivo(orden=self.object, archivo=archivos).save()

        # Generamos el registro
        registro = {
            'orden': self.object,
            'estado': 'Inicial',
            'empleado': self.request.user
        }
        Registro(**registro).save()

        # Guardamos la orden de compra
        self.object.save()

        # Guardamos en el historial del panel de administración
        historial_crear_oc(self.request.user, self.object)

        # Devolvemos a la URL de éxito (lista de órdenes de compra)
        return HttpResponseRedirect(self.get_success_url())


#pagar orden de compra
@method_decorator(login_required,'dispatch')
class OrdenDeCompraPagar(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'ordendecompra.actualizar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            orden = get_object_or_404(OrdenDeCompra,pk=kwargs.get('pk'))
            if orden.pagada != True:
                orden.pagada = True
                orden.save()
            return JsonResponse({'estado':'ok'})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})


#Eliminar
@method_decorator(login_required,'dispatch')
class OrdenDeCompraEliminar(ValidatePermissionRequiredMixin,RedirectView):
    #permiso necesario
    permission_required = 'ordendecompra.eliminar'
    
    #al momento de ejecutar el redirect
    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('ordendecompra.eliminar'):
            print(kwargs.get('pk'))
            #obtenemos la orden
            orden = get_object_or_404(OrdenDeCompra,pk=kwargs.get('pk'))
            print(orden)
            #guardamos en el historial quien la borro
            historial_eliminar_oc(self.request.user,orden)
            #la borramos
            orden.delete()
            #retornamos la lista
        return HttpResponseRedirect(reverse('ordendecompra:lista') + "?mensaje=La orden de compra ha sido eliminada&tipo_mensaje=info")
#Rechazar
@method_decorator(login_required,'dispatch')
class OrdenDeCompraRechazar(ValidatePermissionRequiredMixin,RedirectView):
    #permiso necesario
    permission_required = 'ordendecompra.rechazar'

    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para rechazar la orden de compra.'

    #antes de devolver el redirect
    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('ordendecompra.rechazar'):
            #si no esta la primary key in kwargs, la seteamos como -1 para que tire error 404 (no encontrado)
            if 'pk' not in kwargs:
                kwargs['pk'] = -1
            #obtenemos la orden
            orden = get_object_or_404(OrdenDeCompra,pk=kwargs.get('pk'))
            #guardamos en el historial de administración el rechazo
            historial_rechazar_oc(self.request.user,orden)
            #cambiamos el estado
            orden.estado = 'Rechazada'
            #guardamos la orden
            orden.save()
            #registramos los cambios en el historial del orden de compra
            registrarCambioEstado(orden,self.request.user)
            #devolvemos la lista
        return HttpResponseRedirect(reverse('ordendecompra:lista') + "?rechazada={}".format(orden.numero))


#Editar orden en estado inicial
@method_decorator(login_required, 'dispatch')
class OrdenDeCompraEditarView(ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'ordendecompra.crear'
    #modelo de la orden de compra
    model = OrdenDeCompra
    #la plantilla que se utilizara
    template_name = 'ordendecompra/editar.html'
    #formulario para editar la orden de compra
    form_class = OrdenDeCompraCreateForm
    #la ruta de exito al validar la orden
    success_url = reverse_lazy('ordendecompra:lista')
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para editar la orden de compra'

    #checkear si la orden esta en estado inicial
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado == 'Inicial':
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    def form_valid(self,form):
        self.object = form.save()
        self.object.ordendecomprainsumo_set.all().delete()
        #lista de insumos vacia
        insumos = []
        #obtenemos las ids de los insumos a agregar
        ids = self.request.POST.getlist('idinsumo[]')
        #luego su cantidad
        cantidad = self.request.POST.getlist('cantidadinsumo[]')
        #transformamos los campos vacios de cantidad a 0
        cantidad = [verificarCantidad(x) for x in cantidad]
        #sumamos la cantidad de insumos para verificar que al menos haya alguno.
        total = sum([float(x) for x in cantidad])
        #si el total es menor o igual a 0 devolvemos error.
        if total <= 0:
            return super(OrdenDeCompraEditarView, self).form_invalid(form)
        #generamos nuestro objecto orden de compra
        self.object = form.save()
        #obtenemos los detalles y precios
        precioinsumo = self.request.POST.getlist('precioinsumo[]')
        #generamos nuestros insumos con un diccionario
        for i in range(len(ids)):
            insumo = {'orden_id': self.object.id, 'insumo_id': ids[i], 'cantidad': cantidad[i], 'neto': float(precioinsumo[i])}
            if int(insumo['cantidad']) > 0:
                insumos.append(insumo)
        #agregamos nuestros insumos a la orden de compra
        for insumo in insumos:
            o = OrdenDeCompraInsumo(**insumo)
            o.moneda = o.insumo.moneda.valor
            pinsumo = o.insumo
            if pinsumo.moneda.nombre not in ['USD','EUR']:
                pinsumo.precio = o.neto
                pinsumo.save()
            o.save()
        #actualizamos el total neto
        self.object.total_neto = self.object.totalNeto()
        #guardamos los archivos adjuntos
        files = self.request.FILES.getlist('archivos')
        for f in files:
            Archivo(orden=self.object,archivo=f).save()
        #generamos el registro
        registro = {'orden':self.object,'estado':'Inicial','empleado':self.request.user}
        Registro(**registro).save()
        #guardamos la orden de compra
        self.object.save()
        #guardamos en el historial del panel de administración
        historial_crear_oc(self.request.user,self.object)
        #devolvemos a la url de exito (lista de ordenes de compra)
        return HttpResponseRedirect(self.get_success_url())



#Validar
@method_decorator(login_required,'dispatch')
class OrdenDeCompraValidarView(ValidatePermissionRequiredMixin,UpdateView):
    permission_required = 'ordendecompra.validar'
    #Modelo de la orden de compra
    model = OrdenDeCompra
    #la plantilla que se utilizara
    template_name = 'ordendecompra/validar.html'
    #el formulario ubicado en el archivo .forms.py
    form_class = OrdenDeCompraValidarForm
    #la ruta de exito al validar la orden
    success_url = reverse_lazy('ordendecompra:lista')
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para validar la orden de compra'
    
    #checkear si la orden esta en estado inicial
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado == 'Inicial':
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_success_url())

    #obtención de archivos adjuntos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archivos"] = Archivo.objects.filter(orden=self.object).all() 
        return context


    def form_valid(self,form):
        #obtenemos la orden desde el formulario
        self.object = form.save()
        #obtenemos todos los insumos
        insumos = self.object.ordendecomprainsumo_set.all()
        #extraemos los datos provenientes del formulario de insumos
        ids = self.request.POST.getlist('idinsumo[]')
        cantidad = self.request.POST.getlist('cantidadinsumo[]')
        precioinsumo = self.request.POST.getlist('precioinsumo[]')
        #calculamos el total
        total = sum([float(x) for x in cantidad])
        #si el total es menor o igual a 0 devolvemos error.
        if total <= 0:
            for i in insumos:
                i.delete()
        contador = 0
        #agregamos los insumos / actualizamos
        for id in ids:
            insumo = self.object.ordendecomprainsumo_set.filter(pk=id).get()
            if int(cantidad[contador]) <= 0:
                insumo.delete()
            else:
                insumo.cantidad = cantidad[contador]
                insumo.neto = precioinsumo[contador]
                pinsumo = insumo.insumo
                if pinsumo.moneda.nombre not in ['USD','EUR']:
                    pinsumo.precio = insumo.neto
                    pinsumo.save()
                insumo.save()
            contador+=1
        #cambiamos el estado
        self.object.estado = 'Validada'
        #actualizamos el total
        self.object.total_neto = self.object.totalNeto()
        #guardamos los archivos juntos
        files = self.request.FILES.getlist('archivos')
        for f in files:
            Archivo(orden=self.object,archivo=f).save()
        #guardamos en el historial de la orden de compra el cambio de estado
        registrarCambioEstado(self.object,self.request.user)
        #guardamos la orden
        self.object.save()
        #registramos en el panel administrativo el cambio
        historial_cambiar_estado_oc(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url() + "?mensaje=Se ha validado la orden N°{}&tipo_mensaje=info".format(self.object.numero))

#Recepcionar / Semi recepcionar
@method_decorator(login_required,'dispatch')
class OrdenDeCompraRecepcionarView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso necesario
    permission_required = 'ordendecompra.recepcionar'
    #modelo a utilizar
    model = OrdenDeCompra
    #plantilla
    template_name = 'ordendecompra/recepcionar.html'
    #formulario ubicado en el archivo .forms.py
    form_class = OrdenDeCompraRecepcionarForm
    #url al momento de recepcionar / semi recepcionar
    success_url = reverse_lazy('ordendecompra:lista')
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para recepcionar la orden de compra.'

    #checkear si la orden esta en estado validada / semi-recepcionada
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado in ['Validada']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_success_url())

    #obtenemos los archivos adjuntos y los agregamos al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archivos"] = Archivo.objects.filter(orden=self.object).all() 
        return context
    
    
    #al momento de validar el formulario
    def form_valid(self,form):
        #obtenemos la orden
        self.object = form.save(commit=False)
        #información proveniente del apartado de insumos del formulario
        ids = self.request.POST.getlist('idinsumo[]')
        cantidades = self.request.POST.getlist('insumocantidad[]')
        precios = self.request.POST.getlist('precioinsumo[]')
        bultos = self.request.POST.getlist('bultos[]')
        #obtencion de los insumos de la orden de compra
        orden_insumos = self.object.ordendecomprainsumo_set.all()
        #flag para validar si la orden se encuentra recepcionada completamente o semi-recepcionada
        completa = True
        #eliminamos los bultos anteriores
        bultosa = self.object.insumobulto_set.all().delete()
        #recorremos los insumos
        for orden_insumo in orden_insumos:
            try:
                pos = ids.index(str(orden_insumo.id))
                cantidad = int(cantidades[pos])
                precio = float(precios[pos])
                #obtenemos el inventario actual del insumo, si no existe se crea.
                inventario_insumo, created = InventarioInsumo.objects.get_or_create(bodega=self.object.bodega,insumo=orden_insumo.insumo.insumo,defaults={'cantidad': 0})
                #actualizacion de stock
                if(orden_insumo.cantidad_recibida == 0):      
                    inventario_insumo.cantidad += (cantidad * 1)
                else:
                    inventario_insumo.cantidad += (cantidad - orden_insumo.cantidad_recibida) * 1
                orden_insumo.cantidad_recibida = cantidad
                #actualizamos el valor al nuevo neto
                orden_insumo.neto = precio*orden_insumo.insumo.formato
                
                #guardamos el insumo y el inventario
                orden_insumo.save()
                inventario_insumo.save()
                #si no se cumple la cantidad esperada bajamos la flag de completada
                if(orden_insumo.cantidad  * orden_insumo.insumo.formato > cantidad):
                    completa = False
                #creamos los bultos
                #obtenemos los bultos antiguos por insumo
                bultosc = int(bultos[pos])
                for i in range(bultosc):
                    if bultosc == 1:
                        self.object.insumobulto_set.create(insumo=orden_insumo.insumo.insumo,bodega=self.object.bodega,cantidad=orden_insumo.cantidad_recibida,formato=1,formatoo=orden_insumo.insumo.formato)
                    elif bultosc == orden_insumo.cantidad_recibida * orden_insumo.insumo.formato:
                        self.object.insumobulto_set.create(insumo=orden_insumo.insumo.insumo,bodega=self.object.bodega,cantidad=1,formato=1,formatoo=orden_insumo.insumo.formato)
                    else:
                        self.object.insumobulto_set.create(insumo=orden_insumo.insumo.insumo,bodega=self.object.bodega,cantidad=0,formato=1,formatoo=orden_insumo.insumo.formato)
            #si es que ocurre un error
            except Exception as ex:
                print(ex)
                print('Hubo algun error')
                completa = False
        #cambio de estado de la orden
        if completa:
            self.object.estado = 'Recepcionada'
        else:
            self.object.estado = 'Semi-Recepcionada'
        #actualizamos el total neto de la orden de compra
        self.object.total_neto = self.object.totalNeto()
        #guardamos los archivos adjuntos
        files = self.request.FILES.getlist('archivos')
        for f in files:
            Archivo(orden=self.object,archivo=f).save()
        #registro de cambios, se guarda la orden de compra y se redirecciona
        registrarCambioEstado(self.object,self.request.user)
        self.object.save()
        historial_cambiar_estado_oc(self.request.user,self.object)
        return HttpResponseRedirect(reverse_lazy('ordendecompra:etiquetar',kwargs={'pk':self.object.pk}) + "?mensaje=Se ha actualizado el estado de la orden N°{} a {}&tipo_mensaje=info".format(self.object.numero,self.object.estado))

#ETIQUETAR ORDEN DE COMPRA
@method_decorator(login_required, 'dispatch')
class OrdenDeCompraEtiquetarView(ValidatePermissionRequiredMixin,UpdateView):
    permission_required = 'ordendecompra.etiquetar'
    model = OrdenDeCompra
    template_name = 'ordendecompra/etiquetar.html'
    form_class = OrdenDeCompraEtiquetarForm
    success_url = reverse_lazy('ordendecompra:lista')

    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para etiquetar la orden de compra.'

    #checkear si la orden esta en estado validada / semi-recepcionada
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado in ['Semi-Recepcionada','Recepcionada']:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_success_url())
        

    def form_valid(self, form):
        self.object = form.save(commit=False)
        post = self.request.POST
        bultos = [InsumoBulto.objects.filter(pk=int(id)).first() for id in post.getlist('bultoid')]
        cantidadbultos = post.getlist('cantidadbulto')
        for i in cantidadbultos:
            if(i == '0'):
                error = "No puedes crear bultos con 0 unidades."
                return JsonResponse({'estado':'error','mensaje':error})
        loteproveedor= post.getlist('loteproveedor')
        for i in range(len(bultos)):
            cantidad = float(cantidadbultos[i])
            bulto = bultos[i]
            lp = loteproveedor[i]
            if bulto:
                insumo = bulto.ordendecompra.ordendecomprainsumo_set.filter(insumo__insumo=bulto.insumo,insumo__formato=bulto.formatoo).first()
                if insumo:

                    suma = sum([int(cantidadbultos[i]) for i in range(len(cantidadbultos)) if bultos[i].insumo_id == bulto.insumo_id and bultos[i].formatoo == bulto.formatoo])
                    if suma != insumo.cantidad_recibida:
                        error = "La suma total de las cantidades de {} ({} {}) debe ser igual a la cantidad recibida {}.".format(bulto.insumo.nombre,bulto.formatoo,bulto.insumo.unidad,insumo.cantidad_recibida)
                        return JsonResponse({'estado':'error','mensaje':error})
                    bulto.cantidad = cantidad
                    bulto.lotep = lp
                    bulto.save()
        self.object.estado = 'Etiquetada'
        self.object.save()
        return JsonResponse({'estado':'ok','id':self.object.numero})
        

#Generar Etiquetas Ordenes de Compra
class OrdenDeCompraInsumoCodigoView(ValidatePermissionRequiredMixin,DetailView):
    permission_required = 'ordendecompra.etiquetar'
    model = OrdenDeCompra
    template_name = 'ordendecompra/etiquetar.html'
    form_class = OrdenDeCompraEtiquetarForm
    success_url = reverse_lazy('ordendecompra:lista')

    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para etiquetar la orden de compra.'
    
    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if object.estado == 'Etiquetada':      
            return super().dispatch(request, *args, **kwargs)
        raise Http404('La orden no puede ser etiquetada.')

    def get(self, request, *args, **kwargs):
        descargar = self.request.GET.get('descargar')
        oc = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        if descargar is not None:
            response['Content-Disposition'] = 'attachment; filename="{}.pdf'.format(oc.numero)
        dimensiones = (378,196)
        p = canvas.Canvas(response,pagesize=(dimensiones))
        p.setTitle("OC {}".format(oc.numero))
        grupos = []
        agregar = []
        contador = 0
        contadorg = 0
        for bulto in oc.obtenerBultos():
            print(bulto)
            agregar.append(bulto)
            contador+=1
            contadorg+=1
            if contador == 2:
                contador=0
                grupos.append(agregar)
                agregar = []
            if ( (contadorg == len(oc.obtenerBultos())) and ( len(oc.obtenerBultos())%2 != 0) ):
                if len(grupos) > 0 and len(grupos[-1]) == 1:
                    grupos[-1].append(bulto)
                else:
                    grupos.append(bulto)
        print(grupos)
        for grupo in grupos:
            generar_etiqueta(p,oc,grupo)
        p.save()
        return response


#PAGAR ORDEN DE COMPRA
@method_decorator(login_required,'dispatch')
class OrdenDeCompraPagarView(ValidatePermissionRequiredMixin,UpdateView):
    permission_required = 'ordendecompra.pagar'
    model = OrdenDeCompra
    template_name = 'ordendecompra/pagar.html'
    form_class = OrdenDeCompraPagarForm
    success_url = reverse_lazy('ordendecompra:lista')

    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('ordendecompra:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para pagar la orden de compra.'

    #obtención de archivos adjuntos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archivos"] = Archivo.objects.filter(orden=self.object).all() 
        return context

    #checkear si la orden esta en estado Recepcionada
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado == 'Recepcionada':
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    #al momento de validar el formulario
    def form_valid(self,form):
        #obtencion del objeto
        self.object = form.save()
        #cambio del estado
        self.object.estado = 'Pagada'
        #guardamos los archivos adjuntos
        files = self.request.FILES.getlist('archivos')
        for f in files:
            Archivo(orden=self.object,archivo=f).save()
        #cambios en el registro y retorno de la url de exito
        registrarCambioEstado(self.object,self.request.user)
        self.object.save()
        historial_cambiar_estado_oc(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url() + "?mensaje=Se ha pagado la orden N°{}&tipo_mensaje=info".format(self.object.numero))



@method_decorator(login_required,'dispatch')
class OrdenDeCompraEliminarArchivo(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'ordendecompra.eliminararchivo'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            archivo = get_object_or_404(Archivo,pk=kwargs.get('pk'))
            archivo.delete()
            return JsonResponse({'estado':'ok','orden_id':archivo.orden.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Retroceder orden de compra
@method_decorator(login_required,'dispatch')
class OrdenDeCompraRetroceder(ValidatePermissionRequiredMixin,View):
    permission_required = 'ordendecompra.retroceder'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        estados = ['Inicial','Validada','Recepcionada','Etiquetada','Pagada']
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            orden = get_object_or_404(OrdenDeCompra,pk=kwargs.get('pk'))
            estado = orden.estado
            
            if estado == 'Semi-Recepcionada':
                estado = 'Recepcionada'
            if estado == 'Recepcionada':
                #hay que eliminar el inventario que trajo esta orden
                insumos = orden.ordendecomprainsumo_set.all()
                for i in insumos:
                    inventario_insumo, created = InventarioInsumo.objects.get_or_create(bodega=orden.bodega,insumo=i.insumo.insumo,defaults={'cantidad': 0})
                    inventario_insumo.cantidad -= i.cantidad_recibida
                    i.cantidad_recibida = 0
                    i.save()
                    inventario_insumo.save()
            if estado not in ['Inicial','Rechazada']:
                pos = estados.index(estado)
                orden.estado = estados[pos-1]
                if orden.estado == 'Recepcionada':
                    semi = False
                    insumos = orden.ordendecomprainsumo_set.all()
                    for i in insumos:
                        if i.cantidad_recibida != i.cantidad:
                            semi = True
                    if semi:
                        orden.estado = 'Semi-Recepcionada'
                orden.save()
            if estado == 'Rechazada':
                estado_anterior = orden.ultimo_registro()
                if estado_anterior:
                    orden.estado = estado_anterior.estado
                    orden.save()
            registro = {'orden':orden,'estado':orden.estado,'empleado':self.request.user}
            Registro(**registro).save()
            historial_cambiar_estado_oc(self.request.user,orden)
            return HttpResponseRedirect(reverse('ordendecompra:lista') + "?mensaje=La orden de compra n° {} ha retrocedido al estado: {}&tipo_mensaje=info".format(orden.numero,orden.estado))
        else:
            #de caso contraro enviamos fallo.
            return HttpResponseRedirect(reverse('ordendecompra:lista'))
from django.conf import settings
from django.http.response import Http404, HttpResponseRedirect
from inventario.models import InsumoBulto
from produccion.models import CajaLote,EstadoLote
from produccion.functions import generar_codigo
from rest_framework.response import Response
from .functions import historial_create_envio, historial_create_pallet, historial_delete_envio,historial_delete_pallet, historial_update_envio,historial_update_pallet, generar_etiqueta
from .forms import EnvioCreateForm, EnvioRecepcionarForm, PalletCreateForm, PalletUpdateForm, RutaCerrarForm, RutaCreateForm
from .serializers import EnvioSerializer, EnvioSerializerDetalle,PalletSerializer, RutaSerializer
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.urls import reverse_lazy,reverse
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.views.generic import TemplateView, CreateView,UpdateView,View,DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponse,FileResponse
from .models import Envio, InsumoEnvio, LoteEnvio, Pallet, RegistroPallet, Ruta
from produccion.models import Lote
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.pdfgen import canvas
from io import BytesIO
from rest_framework.views import APIView
from datetime import datetime

# Create your views here.

#Api para obtener el listado de los envios
@method_decorator(login_required,'dispatch')
class EnvioViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #objetos a serializar
    queryset = Envio.objects.all()
    #serializer utilizado
    serializer_class = EnvioSerializer
    #permiso necesario
    permission_required = 'logistica.envio.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para listar los envios.'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Envio.objects.order_by('-pk').all()
        return Envio.objects.filter(lugar_o=self.request.user.perfil.lugar).order_by('-pk').all()
    

#Api personalizada para listar los envios que se van a recepcionar
@method_decorator(login_required,'dispatch')
class EnvioRecepcionarListApiView(ValidatePermissionRequiredMixin,ListAPIView):
    #permiso necesario
    permission_required = 'logistica.envio.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para listar los envios.'
    #serializer
    serializer_class = EnvioSerializer
    def get_queryset(self):
        return Envio.objects.filter(lugar_d=self.request.user.perfil.lugar,estado=0).all().order_by('-pk')

#Api personalizada para sacar el detalle de los envios
@method_decorator(login_required,'dispatch')
class EnvioRetrieveApiView(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario
    permission_required = 'logistica.envio.detalle'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para ver el detalle del envio.'
    #serializer
    serializer_class = EnvioSerializerDetalle

    def get_queryset(self):
        return Envio.objects.filter()
    

#Lista de envios
@method_decorator(login_required,'dispatch')
class EnvioListView(ValidatePermissionRequiredMixin,TemplateView):
    #template a utilizar
    template_name = 'logistica/envios/list.html'
    #permiso necesario
    permission_required = 'logistica.envio.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para listar los envios.'
    


#Lista de envios para recepcionar
@method_decorator(login_required,'dispatch')
class EnvioRecepcionarListView(ValidatePermissionRequiredMixin,TemplateView):
    #template a utilizar
    template_name = 'logistica/envios/recepcion.html'
    #permiso necesario
    permission_required = 'logistica.envio.recepcionar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para recepcionar los envios.'

#Detalle de un envio
@method_decorator(login_required,'dispatch')
class EnvioDetailView(ValidatePermissionRequiredMixin,DetailView):
    #permiso necesario
    permission_required = 'logistica.envio.detail'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para ver el detalle de este envio.'
    #modelo
    model = Envio
    #contexto
    context_object_name = "envio"

    def get_template_names(self):
        self.object = self.get_object()
        if self.object.estado:
            return ["logistica/envios/detallesi.html"]
        else:
            return ["logistica/envios/detalleno.html"]

    def get_context_data(self, **kwargs):
        context = super(EnvioDetailView, self).get_context_data(**kwargs)
        registros = RegistroPallet.objects.filter(envio=context['object']).all()
        if context['object'].estado:
            #obtenemos los lotes que se perdieron
            lotes_no = LoteEnvio.objects.filter(envio=context['object'],recepcionado=False).all()
            lotes_si = LoteEnvio.objects.filter(envio=context['object'],recepcionado=True).all()
            context["lotes_no"] = lotes_no
            context["lotes_si"] = lotes_si
            #obtenemos los insumos que se perdieron
            context['insumos_no'] = InsumoEnvio.objects.filter(envio=context['object'],recepcionado=False).all()
            context['insumos_si'] = InsumoEnvio.objects.filter(envio=context['object'],recepcionado=True).all()
        pallets = []
        for r in registros:
            pallets.append(r)
        context['pallets'] = pallets
        insumos = {}
        for i in InsumoEnvio.objects.filter(envio=context['object']).all():
            if i.insumobulto.insumo.id not in insumos.keys():
                insumo = {'estado': i.recepcionado,'bulto': [],'idinsumo': i.insumobulto.insumo.id,'cantidad':0,'insumo':i.insumobulto.insumo,'formato':i.insumobulto.formato,'total':i.insumobulto.total()}
                insumos[i.insumobulto.insumo.id] = insumo
            insumos[i.insumobulto.insumo.id]['bulto'].append(i.insumobulto)
            insumos[i.insumobulto.insumo.id]['cantidad'] += i.insumobulto.total()
        context['insumos'] = insumos
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.perfil.lugar in [self.object.lugar_o,self.object.lugar_d]:
            return super().dispatch(request, *args, **kwargs)
        elif self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

#Resumen de un envio API
@method_decorator(login_required,'dispatch')
class EnvioResumenApi(ValidatePermissionRequiredMixin,APIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'logistica.envio.detalle'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver el detalle del envio.'

    def get(self, request, *args, **kwargs):
        id_envio = kwargs.get('pk')
        envio = get_object_or_404(Envio,pk=int(id_envio))
        lotes = envio.loteenvio_set.filter(recepcionado=True).all()
        insumos = envio.insumoenvio_set.filter(recepcionado=True).all()
        final = {'lotes': [], 'insumos': []}
        for lote in lotes:
            diccionario = {'id': lote.cajalote.lote.producto.id, 'producto': lote.cajalote.lote.producto.nombre, 'unidad': lote.cajalote.lote.producto.unidad, 'presentacion': lote.cajalote.lote.producto.presentacion, 'cajas': 1, 'cantidad': lote.cajalote.cantidad}
            encontrado = False
            for f in final['lotes']:
                if f['id'] == lote.cajalote.lote.producto.id:
                    f['cantidad'] += lote.cajalote.cantidad
                    f['cajas']+=1
                    encontrado = True
            if encontrado == False:
                final['lotes'].append(diccionario)
        for insumo in insumos:
            encontrado = False
            diccionario = {'insumo': insumo.insumobulto.insumo.id,'bultos':1, 'nombre': insumo.insumobulto.insumo.nombre, 'unidad': insumo.insumobulto.insumo.unidad, 'cantidad': insumo.insumobulto.formato * insumo.insumobulto.cantidad}
            for i in final['insumos']:
                if i['insumo'] == insumo.insumobulto.insumo.id:
                    i['bultos']+=1
                    i['cantidad'] += insumo.insumobulto.formato * insumo.insumobulto.cantidad
                    encontrado = True
            if encontrado == False:
                final['insumos'].append(diccionario)    
        return Response({"resumen":final})


#Crear un envio
@method_decorator(login_required,'dispatch')
class EnvioCreateView(ValidatePermissionRequiredMixin,CreateView):
    #template a utilizar
    template_name = 'logistica/envios/create.html'
    #permiso necesario
    permission_required = 'logistica.envio.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para generar un envio.'
    #modelo a utilizar
    model = Envio
    form_class = EnvioCreateForm
    #url de redirección si todo sale bien
    success_url = reverse_lazy('logistica:envios:lista')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'lugar':self.request.user.perfil.lugar})
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.encargado_envio = self.request.user
        self.object.lugar_o = self.request.user.perfil.lugar
        self.object.save()
        #rescatamos los lotes
        lotes = self.request.POST.getlist('lotes[]')
        #rescatamos los pallets
        pallets = self.request.POST.getlist('pallet[]')
        #rescatamos los insumos
        insumos = self.request.POST.getlist('insumos[]')
        #obtenemos los pallets
        pallets = Pallet.objects.filter(pk__in=[int(pallet) for pallet in pallets]).all()
        for pallet in pallets:
            pallet.envio = self.object
            pallet.save()
            pallet.generarRegistro()
        #manejamos los lotes
        for lote in lotes:
            info = lote.split(' ')
            cajalote = CajaLote.objects.filter(lote_id=int(info[0]),caja=int(info[1]),cantidad=int(info[2])).first()
            if cajalote is not None:
                cajalote.estado = 'En Transito'
                cajalote.save()
                loteEnvio = self.object.loteenvio_set.create(cajalote=cajalote)
        #manejamos los insumos
        insumos = InsumoBulto.objects.filter(pk__in=[int(insumo) for insumo in insumos]).filter(bodega=self.request.user.perfil.lugar).all()
        for i in insumos:
            bulto = self.object.insumoenvio_set.create(insumobulto=i)
            i.enviar()
        for l in lotes:
            info = l.split(' ')
            lote = Lote.objects.filter(pk=int(info[0])).first()
            if lote is not None:
                lote.transito(self.request.user,self.object)
        historial_create_envio(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())

#Retroceder Envio
@method_decorator(login_required,'dispatch')
class EnvioRetrocederView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'logistica.envio.retroceder'
    url_redirect = reverse_lazy('logistica:envio:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para retroceder este envio.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            envio = get_object_or_404(Envio,pk=kwargs.get('pk'))
            if envio.estado:
                bultos = envio.insumoenvio_set.all()
                for b in bultos:
                    if b.recepcionado:
                        b.manejarinventario(envio.lugar_d,'restar')
                    b.recepcionado = None
                    b.save()
                envio.estado = False
                envio.save()
                return JsonResponse({'estado':'ok','envio':envio.id})
            else:
                return JsonResponse({'estado':'fallo'})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Etiquetas un envio
@method_decorator(login_required,'dispatch')
class EnvioEtiquetasView(ValidatePermissionRequiredMixin,DetailView):
    permission_required = 'logistica.envio.etiquetas'
    model = Envio
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver las etiquetas del envio.'

    def get(self, request, *args, **kwargs):
        envio = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf'.format(envio.pk)
        dimensiones = (378,196)
        p = canvas.Canvas(response,pagesize=(dimensiones))
        p.setTitle("Envio {}".format(envio.pk))
        grupos = []
        agregar = []
        contador = 0
        contadorg = 0
        #bultos
        for bulto in envio.insumoenvio_set.all():
            agregar.append(bulto.insumobulto)
            contador+=1
            contadorg+=1
            if contador == 2:
                contador=0
                grupos.append(agregar)
                agregar = []
            if ( (contadorg == len(envio.insumoenvio_set.all())) and ( len(envio.insumoenvio_set.all())%2 != 0) ):
                if len(grupos) > 0 and len(grupos[-1]) == 1:
                    grupos[-1].append(bulto.insumobulto)
                else:
                    grupos.append(bulto.insumobulto)
        print(grupos)
        for grupo in grupos:
            generar_etiqueta(p,grupo)
        #productos
        contador = 1
        for lote in envio.loteenvio_set.all():
            self.object = lote.cajalote
            generar_codigo(p,self.object,contador,self.object.cantidad)
        p.save()
        return response

#Recepcionar un envio
@method_decorator(login_required,'dispatch')
class EnvioRecepcionarView(ValidatePermissionRequiredMixin,UpdateView):
    #template a utilizar
    template_name = 'logistica/envios/recepcionar.html'
    #permiso necesario
    permission_required = 'logistica.envio.recepcionar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para recepcionar un envio.'
    #modelo a utilizar
    model = Envio
    #formulario a utilizar
    form_class = EnvioRecepcionarForm

    #verificación que la persona esta en el lugar de destino, y el envio no ha sido recepcionado
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.lugar_d == self.request.user.perfil.lugar and self.object.estado == 0:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
    
    def form_valid(self, form):
        #actualizamos el envio
        self.object = form.save()
        #colocamos su estado en true
        self.object.estado = True
        self.object.encargado_recepcion = self.request.user
        #guardamos el envio
        self.object.save()
        #obtenemos los lotes que no se recibieron
        lotes = self.request.POST.getlist('lotes[]')
        #obtenemos los pallets que no se recibieron
        pallets = self.request.POST.getlist('pallet[]')
        #obtenemos los insumos que no se recibieron
        bultos = [int(b) for b in self.request.POST.getlist('bultos[]')]
        #obtenemos los pallets del envio
        pallets_envio = self.object.pallet_set.all()
        lotes_envio = self.object.loteenvio_set.all()
        bultos_envio = self.object.insumoenvio_set.all()
        #generamos una lista con los ids de los lotes y sus cajas
        pallets_id = [str(p.id) for p in pallets_envio]
        lotes_id = ["{}  {}  {}".format(l.cajalote.lote.id,l.cajalote.caja,l.cajalote.cantidad) for l in lotes_envio]
        #generamos una lista con los ids de los bultos
        bultos_id = [int(b.insumobulto.id) for b in bultos_envio]
        #vemos que se recepciono y que no se recepciono
        lotes_recepcionados = list(set(lotes_id) - set(lotes))
        lotes_no_recepcionados = list(set(lotes_id) - set(lotes_recepcionados))
        pallets_recepcionados = list(set(pallets_id) - set(pallets))
        pallets_no_recepcionados = list(set(pallets_id) - set(pallets_recepcionados))
        bultos_recepcionados = list(set(bultos_id) - set(bultos))
        bultos_no_recepcionados = list(set(bultos_id) - set(bultos_recepcionados))
        #BULTOS NO RECEPCIONADOS
        for bultor in bultos_no_recepcionados:
            try:
                bulto = [bulto for bulto in bultos_envio if bulto.insumobulto.id == bultor][0]
                bulto.recepcionado = False
                bulto.save()
            except Exception as ex:
                print(ex)
        #BULTOS RECEPCIONADOS
        for bultor in bultos_recepcionados:
            try:
                bulto = [bulto for bulto in bultos_envio if bulto.insumobulto.id == bultor][0]
                bulto.recepcionado = True
                bulto.save()
                insumo = bulto.insumobulto
                insumo.recepcionar(self.object.lugar_d)
            except Exception as ex:
                print(ex)
        #LOTES NO RECEPCIONADOS
        for loter in lotes_no_recepcionados:
            info = [int(l) for l in loter.split("  ")]
            try:
                l = [lote for lote in lotes_envio if (lote.cajalote.lote.id == info[0] and lote.cajalote.caja == info[1] and lote.cajalote.cantidad == info[2])][0]
                l.recepcionado = False
                l.pallet = None
                l.cajalote.lugar = None
                l.cajalote.estado = 'Extraviado'
                l.cajalote.save()
                l.save()
            except:
                continue
        #LOTES RECEPCIONADOS
        for loter in lotes_recepcionados:
            info = [int(l) for l in loter.split("  ")]
            try:
                l = [lote for lote in lotes_envio if (lote.cajalote.lote.id == info[0] and lote.cajalote.caja == info[1] and lote.cajalote.cantidad == info[2])][0]
                l.recepcionar()
            except:
                continue
        #PALLETS NO RECEPCIONADOS
        for palletr in pallets_no_recepcionados:
            try:
                p = [pallet for pallet in pallets_envio if str(pallet.id) == palletr][0]
                p.lugar = None
                p.envio = None
                p.save()
                p.finalizarRegistro(False)
            except:
                continue
        #PALLETS RECEPCIONADOS
        for palletr in pallets_recepcionados:
            try:
                p = [pallet for pallet in pallets_envio if str(pallet.id) == palletr][0]
                p.lugar= p.envio.lugar_d
                p.envio = None
                p.save()
                p.finalizarRegistro(True)
            except:
                continue
        lotes = self.object.obtener_lotes()
        for l in lotes:
            l.recepcionado(self.request.user,self.object)
        historial_update_envio(self.request.user,self.object,"recepcionado")
        return HttpResponseRedirect(reverse_lazy('logistica:envios:detalle',kwargs={'pk':self.object.id}))

#Eliminar Envio
@method_decorator(login_required,'dispatch')
class EnvioDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'logistica.envio.eliminar'
    url_redirect = reverse_lazy('logistica:envio:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este envio.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            envio = get_object_or_404(Envio,pk=kwargs.get('pk'))
            if envio.estado in [True,False]:
                historial_delete_envio(self.request.user,envio)
                envios = envio.loteenvio_set.all()
                pallet = envio.registropallet_set.all()
                for p in pallet:
                    if p == p.pallet.registropallet_set.last():
                        p.pallet.lugar = envio.lugar_o
                        p.pallet.save()
                envio.delete()
                return JsonResponse({'estado':'ok','envio':envio.id})
            else:
                return JsonResponse({'estado':'fallo'})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})
# PALLETS #
#Api para obtener el listado de los pallets
@method_decorator(login_required,'dispatch')
class PalletViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #objetos a serializar
    queryset = Pallet.objects.all()
    #serializer utilizado
    serializer_class = PalletSerializer
    #permiso necesario
    permission_required = 'logistica.pallet.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para listar los pallets.'

#API PARA OBTENER EL DETALLE DE CADA LOTE
@method_decorator(login_required,'dispatch')
class PalletRetrieveApi(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'logistica.pallet.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los pallets.'
    serializer_class = PalletSerializer

    def get_queryset(self):
        return Pallet.objects.filter()

#API Para Consultar estado de pallet al momento de escanear
@method_decorator(login_required,'dispatch')
class PalletRetrieveScanApi(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'logistica.pallet.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los pallets.'
    serializer_class = PalletSerializer

    def get_queryset(self):
        pallet = Pallet.objects.filter(lugar=self.request.user.perfil.lugar,envio=None)
        return pallet

#Lista de Pallets
@method_decorator(login_required,'dispatch')
class PalletListView(ValidatePermissionRequiredMixin,TemplateView):
    #template a utilizar
    template_name = 'logistica/pallets/list.html'
    #permiso necesario
    permission_required = 'logistica.pallet.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para listar los pallets.'

#Crear un Pallet
@method_decorator(login_required,'dispatch')
class PalletCreateView(ValidatePermissionRequiredMixin,CreateView):
    #template a utilizar
    template_name = 'logistica/pallets/create.html'
    #permiso necesario
    permission_required = 'logistica.pallet.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para agregar un pallet.'
    #modelo a utilizar
    model = Pallet
    #formulario de creación a utilizar
    form_class = PalletCreateForm
    #url de redirección
    success_url = reverse_lazy('logistica:pallet:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_create_pallet(self.request.user,self.object)
        return super().form_valid(form)

#Generar el codigo de barra del pallet
@method_decorator(login_required,'dispatch')
class PalletCodigoView(ValidatePermissionRequiredMixin,DetailView):
    #template a utilizar
    template_name = 'logistica/pallets/barra.html'
    #permiso necesario
    permission_required = 'logistica.pallet.detalle'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para ver el detalle de un pallet.'
    #modelo a utilizar
    model = Pallet


    def get(self, request, *args, **kwargs):
        pallet = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{}.pdf'.format(pallet.nombre)
        dimensiones = (109*mm,110*mm)
        rv = BytesIO()
        p = canvas.Canvas(response,pagesize=dimensiones)
        p.setTitle("{}".format(pallet.nombre))
        
        bar_class = barcode.get_barcode_class('code128')
        barcoded = '{}  {}'.format("P",pallet.id)
        writer=ImageWriter()
        code128 = bar_class(barcoded, writer)
        code128.write(rv, {"module_width":0.35, "module_height":10, "font_size": 10, "text_distance": 1, "quiet_zone": 3})
        image = ImageReader(rv)
        #image = image.resize(image,100,100)
        p.drawImage(image,0,0,dimensiones[0],dimensiones[1],None,True)
        p.showPage()

        p.save()
        pdf = rv.getvalue()
        rv.close()
        response.write(pdf)
        return response

#Actualizar un Pallet
@method_decorator(login_required,'dispatch')
class PalletUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #template a utilizar
    template_name = 'logistica/pallets/create.html'
    #permiso necesario
    permission_required = 'logistica.pallet.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para actualizar un pallet.'
    #modelo a utilizar
    model = Pallet
    #formulario de creación a utilizar
    form_class = PalletUpdateForm
    #url de redirección
    success_url = reverse_lazy('logistica:pallet:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_update_pallet(self.request.user,self.object)
        return super().form_valid(form)

#Eliminar un Pallet
@method_decorator(login_required,'dispatch')
class PalletDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'logistica.pallet.eliminar'
    url_redirect = reverse_lazy('logistica:pallet:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este pallet.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            pallet = get_object_or_404(Pallet,pk=kwargs.get('pk'))
            historial_delete_pallet(self.request.user,pallet)
            pallet.delete()
            return JsonResponse({'estado':'ok','pallet':pallet.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Api para obtener el listado de las rutas
@method_decorator(login_required,'dispatch')
class RutaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #objetos a serializar
    queryset = Ruta.objects.all()
    #serializer utilizado
    serializer_class = RutaSerializer
    #permiso necesario
    permission_required = 'logistica.rutas.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para listar las rutas.'

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Ruta.objects.all()
        username = self.request.query_params.get('usuario')
        abierta = self.request.query_params.get('abierto')
        if username is not None:
            queryset = queryset.filter(persona_id=int(username))
        if abierta is not None:
            queryset = queryset.filter(estado='Abierto')
        return queryset

#Lista de rutas
@method_decorator(login_required, 'dispatch')
class RutaListView(ValidatePermissionRequiredMixin, TemplateView):
    #permiso necesario
    permission_required = 'logistica.rutas.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para listar las rutas.'
    #template a utilizar
    template_name = 'logistica/rutas/list.html'

#Crear Ruta
@method_decorator(login_required, 'dispatch')
class RutaCreateView(ValidatePermissionRequiredMixin, CreateView):
    #permiso necesario
    permission_required = 'logistica.rutas.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para crear una ruta.'
    #template a utilizar
    template_name = 'logistica/rutas/create.html'
    #formulario a utilizar
    form_class = RutaCreateForm
    #url de redirección
    success_url = reverse_lazy('logistica:rutas:lista')

#Actualizar Ruta
@method_decorator(login_required, 'dispatch')
class RutaUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    #permiso necesario
    permission_required = 'logistica.rutas.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para actualizar una ruta.'
    #template a utilizar
    template_name = 'logistica/rutas/create.html'
    #formulario a utilizar
    form_class = RutaCreateForm
    #url de redirección
    success_url = reverse_lazy('logistica:rutas:lista')
    #modelo a utilizar
    model = Ruta

#Cerrar Ruta
@method_decorator(login_required,'dispatch')
class RutaCerrarView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso necesario
    permission_required = 'logistica.rutas.cerrar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para cerrar una ruta.'
    #template a utilizar
    template_name = 'logistica/rutas/cerrar.html'
    #formulario a utilizar
    form_class = RutaCerrarForm
    #url de redirección
    success_url = reverse_lazy('logistica:rutas:lista')
    #modelo a utilizar
    model = Ruta

    def dispatch(self, request, *args, **kwargs):
        ruta = self.get_object()
        if ruta.estado != 'Abierto':
            raise Http404('La ruta ya se encuentra cerrada.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context['rutas'] = Ruta.objects.filter(estado='Abierto').exclude(pk=self.object.id).all()
        return context

    def post(self,request,*args,**kwargs):
        objeto = self.get_object()
        if objeto.estado == 'Abierto':
            #verificamos que no posea ordenes no entregadas o asignadas
            ordenes = objeto.rutaov_set.filter(orden__estado__in=['No Entregado','Asignado']).all()
            if len(ordenes) != 0:
                return JsonResponse({'estado':'error','mensaje':'La ruta no puede ser cerrada ya que posee ordenes activas.'})
            objeto.estado = 'Cerrado'
            objeto.save()
            return JsonResponse({'estado':'ok','mensaje':'La ruta ha sido cerrada existosamente.'})
        return JsonResponse({'estado':'error','mensaje':'La ruta no esta abierta.'})

    def form_valid(self, form):

        return HttpResponseRedirect(self.get_success_url())

#Eliminar Ruta
@method_decorator(login_required,'dispatch')
class RutaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'logistica.rutas.eliminar'
    url_redirect = reverse_lazy('logistica:rutas:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar esta ruta.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            ruta = get_object_or_404(Ruta,pk=kwargs.get('pk'))
            #obtenemos las ov
            ovs = ruta.rutaov_set.all()
            for ov in ovs:
                if ov.orden.estado == 'Asignado':
                    facturas = ov.orden.get_facturas()
                    boleta = False
                    for f in facturas:
                        if settings.IDENTIFICADOR_BOLETA in f:
                            boleta = True
                    if boleta:
                        ov.orden.estado = 'Boleteado'
                    else:
                        ov.orden.estado = 'Facturado'
                    ov.orden.save()
            ovs.delete()
            #historial_delete_pallet(self.request.user,pallet)
            ruta.delete()
            return JsonResponse({'estado':'ok','ruta':ruta.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Mis Rutas
@method_decorator(login_required, 'dispatch')
class MisRutasView(ValidatePermissionRequiredMixin,TemplateView):
    #permiso
    permission_required = 'logistica.rutas.misrutas'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver tus rutas.'
    template_name = 'logistica/repartidor/misrutas.html'

#Seguimiento Ruta
@method_decorator(login_required, 'dispatch')
class RutaSeguimientoView(ValidatePermissionRequiredMixin,DetailView):
    #permiso
    permission_required = 'logistica.rutas.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para las rutas.'
    template_name = 'logistica/rutas/seguimiento.html'
    model = Ruta

#Detalle Ruta
@method_decorator(login_required, 'dispatch')
class RutaDetailView(ValidatePermissionRequiredMixin,DetailView):
    #permiso
    permission_required = 'logistica.rutas.misrutas'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver tus rutas.'
    template_name = 'logistica/rutas/detail.html'
    model = Ruta

    def dispatch(self, request, *args, **kwargs):
        ruta = super().get_object()
        if ruta.persona != self.request.user:
            raise Http404('La ruta no te pertenece')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ruta = context['object']
        context["ordenes_a"] =  ruta.rutaov_set.exclude(orden__estado='Entregado').exclude(orden__estado='Recepción Parcial').exclude(orden__estado='No Entregado').all()
        context["ordenes_e"] = ruta.rutaov_set.filter(orden__estado__in=['Entregado', 'Recepción Parcial', 'No Entregado']).all()
        return context



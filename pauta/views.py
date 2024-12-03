from .functions import historial_actualizar_parametro_pauta, historial_actualizar_pauta, historial_crear_parametro_pauta, historial_crear_pauta, historial_eliminar_parametro_pauta, historial_eliminar_pauta
from .forms import ColumnaForm, PautaForm
from .serializers import ColumnaSerializer, PautaElaboracionSerializer, PautaSerializer
from nucleo.models import Insumo
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,CreateView,DetailView,View,UpdateView
from rest_framework import viewsets, mixins
from rest_framework.generics import RetrieveAPIView
from .models import Columna, Etapa, Instruccion, Pauta, InstruccionColumna, Ingrediente
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.http.response import HttpResponseRedirect

# Create your views here.

#API PARA OBTENER LA PAUTA DE INSUMO DESDE ELABORACION
@method_decorator(login_required,'dispatch')
class PautaElaboracionRetrieve(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #serializador
    serializer_class = PautaElaboracionSerializer
    queryset = Pauta.objects.filter()
    permission_required = 'produccion.pauta.detalle'

    def get_serializer_context(self):
        context = super(PautaElaboracionRetrieve, self).get_serializer_context()
        context.update({'lugar': self.kwargs.get('lugar')})
        return context
    
@method_decorator(login_required,'dispatch')
class PautaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'pauta.listar'
    #las ordenes de compras que seran mostradas en la api rest
    queryset = Pauta.objects.all()
    serializer_class = PautaSerializer

#Lista de pautas
@method_decorator(login_required,'dispatch')
class PautaTemplateView(ValidatePermissionRequiredMixin,TemplateView):
    #permiso requerido para la vista
    permission_required = 'pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las pautas.'
    #template
    template_name = 'pauta/pauta-list.html'

#Detalle Pauta
@method_decorator(login_required,'dispatch')
class PautaDetailView(ValidatePermissionRequiredMixin,DetailView):
    #permiso requerido para la vista
    permission_required = 'pauta.detalle'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver el detalle de esta pauta.'
    #template
    template_name = 'pauta/pauta-detail.html'
    context_object_name = 'pauta'
    model = Pauta

#Crear Pauta
@method_decorator(login_required,'dispatch')
class PautaCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso para la vista
    permission_required = 'pauta.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:pauta:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una pauta.'
    #template
    template_name = 'pauta/pauta-create.html'
    #modelo
    model = Pauta
    #formulario
    form_class = PautaForm
    #url de exito
    success_url = reverse_lazy('administrador:pauta:lista')


    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['columnas'] = Columna.objects.all()
       return context


    def get_success_url(self):
        return super().get_success_url() + "?tipo=info&mensaje=Se ha añadido la pauta correctamente."

    def form_valid(self, form):
        # guardamos la pauta base
        self.object = form.save()
        productos = [int(id) for id in self.request.POST.getlist('productos')]
        for p in productos:
            self.object.pautaproducto_set.create(producto_id=p)
        # sacamos los ingredientes
        ingredientes = self.request.POST.getlist('ingredientes[]')
        ingredientes_c = self.request.POST.getlist('ingredientes_c[]')
        ingredientes_u = self.request.POST.getlist('ingredientes_u[]')
        ingredientes_o = self.request.POST.getlist('ingredientes_o[]')
        ingredientes_l = self.request.POST.getlist('ingredientes_l[]')
        ips = self.request.POST.getlist('insumosp[]')
        checklider = False
        # Agregar Ingredientes
        for index, ingrediente in enumerate(ingredientes):
            cantidad = ingredientes_c[index]
            unidad = ingredientes_u[index]
            if(unidad == ''):
                continue
            opcional = True if ingredientes_o[index] == '1' else False
            lider = True if ingredientes_l[index] == '1' else True
            if lider:
                if checklider:
                    lider = False
                opcional = False
            try:
                if float(cantidad) > 0:
                    ing = Ingrediente(**{'cantidad':cantidad,'insumo_id':ingrediente,'pauta_id':self.object.id,'unidad':unidad,'opcional':opcional,'lider':lider})
                    ing.save()
            except:
                print("Error en el ingrediente")
            if lider:
                checklider = True
        #Agregar IPS
        for id in ips:
            #buscamos el insumo
            insumo = Insumo.objects.filter(pk=int(id)).first()
            if insumo:
                self.object.insumoproceso_set.create(insumo=insumo)
        #Agregar Etapas
        etapas = self.request.POST.getlist('etapas[]')
        for indexe,etapa in enumerate(etapas):
            #obtenemos las columnas
            etapaF = Etapa(**{'orden':indexe,'nombre':etapa,'pauta_id':self.object.id})
            etapaF.save()
            instrucciones = self.request.POST.getlist("ietapa{}[]".format(indexe))
            #Agregar Instrucciones
            for indexi,instruccion in enumerate(instrucciones):
                ins = Instruccion(**{'orden':indexi,'etapa_id':etapaF.pk,'descripcion':instruccion})
                ins.save()
                #Agregar Columnas a Instrucciones
                for columna in self.request.POST.getlist(f'columnas_etapa{indexe}i{indexi}'):
                    insc = InstruccionColumna(**{'instruccion_id':ins.pk,'columna_id':columna})
                    insc.save()
        historial_crear_pauta(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())

#Actualizar Pauta
@method_decorator(login_required,'dispatch')
class PautaUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso para la vista
    permission_required = 'pauta.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:pauta:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una pauta.'
    #template
    template_name = 'pauta/pauta-update.html'
    #modelo
    model = Pauta
    #formulario
    form_class = PautaForm
    #url de exito
    success_url = reverse_lazy('administrador:pauta:lista')
    context_object_name = 'pauta'

    def get_success_url(self):
        return super().get_success_url() + "?tipo=info&mensaje=Se ha actualizado la pauta correctamente."
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['columnas'] = Columna.objects.all()
       return context

    def form_valid(self, form):
        #guardamos el objecto
        self.object = form.save()
        #ACTUALIZAR INGREDIENTES
        #obtenemos los ingredientes
        ingredientes = self.request.POST.getlist('ingredientes[]')
        ingredientes_c = self.request.POST.getlist('ingredientes_c[]')
        ingredientes_u = self.request.POST.getlist('ingredientes_u[]')
        ingredientes_o = self.request.POST.getlist('ingredientes_o[]')
        ingredientes_l = self.request.POST.getlist('ingredientes_l[]')
        ips = self.request.POST.getlist('ips[]')
        #obtenemos los ingredientes Actuales
        ingredientesA = self.object.ingrediente_set.all()
        por_eliminar = []
        checklider = False
        for index, ingrediente in enumerate(ingredientes):
            # confirmar si existe ya el ingrediente
            existe = ingredientesA.filter(insumo__pk=ingrediente).first()
            cantidad = float(ingredientes_c[index])
            unidad = ingredientes_u[index]
            if(unidad == ''):
                continue
            opcional = False if ingredientes_o[index] == '0' else True
            lider = False if ingredientes_l[index] == '0' else True
            if lider:
                if (checklider):
                    lider = False
                opcional = False
            if existe:
                if cantidad > 0:
                    existe.cantidad = cantidad
                    existe.opcional = opcional
                    existe.lider = lider
                    existe.unidad = unidad
                    existe.save()
                else:
                    por_eliminar.append(existe.pk)
            else:
                if cantidad > 0:
                    ing = Ingrediente(**{'cantidad':cantidad,'insumo_id':ingrediente,'pauta_id':self.object.id,'unidad':unidad,'opcional':opcional,'lider':lider})
                    ing.save()
            if lider:
                checklider = True
        #eliminamos los que tuvieron 0 en algun momento
        for eliminar in por_eliminar:
            ingredientesA.filter(pk=eliminar).delete()
        [ingrediente.delete() for ingrediente in ingredientesA if str(ingrediente.insumo.id) not in ingredientes]
        etapas = self.request.POST.getlist('etapas[]')
        id_etapas = self.request.POST.getlist('etapasidentificador[]')
        #obtenemos las etapas actuales
        etapasA = self.object.etapa_set.all()
        #eliminamos las etapas no actuales
        [etapa.delete() for etapa in etapasA if str(etapa.pk) not in id_etapas]
        #actualizamos las etapas actuales
        etapasA = self.object.etapa_set.all()
        for index,etapa in enumerate(etapas):
            #confirmar si existe la etapa
            indice = id_etapas[index]
            try:
                int(indice)
            except:
                indice = -900
            existe = etapasA.filter(pk = indice).first()
            if existe:
                existe.nombre = etapas[index]
                existe.save()
                #procedemos a ver las instrucciones asociadas
                instrucciones = self.request.POST.getlist('ietapa{}[]'.format(index))
                id_instrucciones = self.request.POST.getlist('ietapai{}[]'.format(index))
                #obtenemos las instrucciones
                instruccionesA = existe.instruccion_set.all()
                for indexi,instruccion in enumerate(instrucciones):
                    #ver si existe la instruccion
                    identificador_instruccion = id_instrucciones[indexi]
                    try:
                        int(identificador_instruccion)
                    except:
                        identificador_instruccion = -900
                    instruccionF = instruccionesA.filter(pk=identificador_instruccion).first()
                    if instruccionF:
                        instruccionF.descripcion = instruccion
                        instruccionF.save()
                        instruccion_columnas = instruccionF.instruccioncolumna_set.all()
                        #tengo las columnas asociadas al objeto
                        #tengo las instruccionescolumnas del la instruccion
                        #
                        columnas = [int(x) for x in self.request.POST.getlist(f'columnas_etapa{index}i{indexi}')]
                        for columna in columnas:
                            #ver si existe la columna
                            existe_columna = instruccion_columnas.filter(columna_id=columna).first()
                            if not existe_columna:
                                insc = InstruccionColumna(**{'instruccion_id':instruccionF.pk,'columna_id':columna})
                                insc.save()
                        #eliminar las columnas que ya no existen
                        [instruccion_columna.delete() for instruccion_columna in instruccion_columnas if instruccion_columna.columna.id not in columnas]
                    else:
                        ins = Instruccion(**{'orden':indexi,'etapa_id':existe.pk,'descripcion':instruccion})
                        ins.save()
                        id_instrucciones.append(str(ins.pk))
                        #Agregar Columnas a Instrucciones
                        columnas = [int(x) for x in self.request.POST.getlist(f'columnas_etapa{index}i{indexi}')]
                        for columna in columnas:
                            insc = InstruccionColumna(**{'instruccion_id':ins.pk,'columna_id':columna})
                            insc.save()
                #eliminar las instrucciones que ya no existen
                [instruccionA.delete() for instruccionA in instruccionesA if str(instruccionA.pk) not in id_instrucciones]
            #si no existe la etapa se procede a crear
            else:
                etapaF = Etapa(**{'orden':index,'nombre':etapa,'pauta_id':self.object.id})
                etapaF.save()
                instrucciones = self.request.POST.getlist('ietapa{}[]'.format(index))
                for indexi,instruccion in enumerate(instrucciones):
                    ins = Instruccion(**{'orden':indexi,'etapa_id':etapaF.pk,'descripcion':instruccion})
                    ins.save()
                    #Agregar Columnas a Instrucciones
                    columnas = [int(x) for x in self.request.POST.getlist(f'columnas_etapa{index}i{indexi}')]
                    for columna in columnas:
                        insc = InstruccionColumna(**{'instruccion_id':ins.pk,'columna_id':columna})
                        insc.save()
        #obtenemos los ips antiguos
        for ip in ips:
            insumop = Insumo.objects.filter(pk=int(ip)).first()
            #check si existe
            if insumop is not None:
                if self.object.insumoproceso_set.filter(insumo__id=insumop.pk).first() is None:
                    self.object.insumoproceso_set.create(insumo=insumop)
        insumoprocesos = self.object.insumoproceso_set.all()
        for insumo in insumoprocesos:
            if str(insumo.insumo.pk) not in ips:
                insumo.delete()
        productos = [int(id) for id in self.request.POST.getlist('productos')]
        for p in productos:
            existe = self.object.pautaproducto_set.filter(producto_id=p).first()
            if existe is None:
                producto = self.object.pautaproducto_set.create(producto_id=p)
                p = existe.producto
                p.pautalinea = self.object
                p.save()
        diferencia = [producto for producto in self.object.pautaproducto_set.all() if producto.producto.id not in productos]
        for d in diferencia:
            producto = d.producto
            producto.pautalinea = None
            producto.save()
            d.delete()
        historial_actualizar_pauta(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())
#Eliminar pauta
@method_decorator(login_required,'dispatch')
class PautaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'pauta.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            pauta = get_object_or_404(Pauta,pk=kwargs.get('pk'))
            historial_eliminar_pauta(self.request.user,pauta)
            pauta.delete()
            return JsonResponse({'estado':'ok','pauta':pauta.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})


#Api de columnas
@method_decorator(login_required,'dispatch')
class ColumnaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'pauta.columna.listar'
    #las ordenes de compras que seran mostradas en la api rest
    queryset = Columna.objects.all()
    serializer_class = ColumnaSerializer

#Lista de Columnas
@method_decorator(login_required,'dispatch')
class ColumnaListView(ValidatePermissionRequiredMixin,TemplateView):
    #permiso para la vista
    permission_required = 'pauta.columna.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:pauta:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las columna.'
    #template
    template_name = 'pauta/columna-list.html'

#Crear Columna
@method_decorator(login_required,'dispatch')
class ColumnaCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso para la vista
    permission_required = 'pauta.columna.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:pauta:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una columna.'
    #template
    template_name = 'pauta/columna-create.html'
    #modelo
    model = Columna
    #formulario
    form_class = ColumnaForm
    #url de exito
    success_url = reverse_lazy('administrador:pauta:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_crear_parametro_pauta(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return super().get_success_url() + "?tipo=info&mensaje=Se ha creado el parametro correctamente."

#Actualizar Columna
@method_decorator(login_required,'dispatch')
class ColumnaUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso para la vista
    permission_required = 'pauta.columna.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:pauta:columna')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar la columna.'
    #template
    template_name = 'pauta/columna-update.html'
    #modelo
    model = Columna
    #formulario
    form_class = ColumnaForm
    #url de exito
    success_url = reverse_lazy('administrador:pauta:columna')

    def form_valid(self, form):
        self.object = form.save()
        historial_actualizar_parametro_pauta(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return super().get_success_url() + "?tipo=info&mensaje=Se ha actualizado el parametro correctamente."

#Eliminar columna
@method_decorator(login_required,'dispatch')
class ColumnaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'pauta.columna.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            columna = get_object_or_404(Columna,pk=kwargs.get('pk'))
            historial_eliminar_parametro_pauta(self.request.user,columna)
            columna.delete()
            return JsonResponse({'estado':'ok','columna':columna.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

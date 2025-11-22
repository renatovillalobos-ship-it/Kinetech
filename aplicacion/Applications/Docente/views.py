from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth.mixins import LoginRequiredMixin --> no se está utilizando
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
#from django.db.models import Avg  --> no se está utilizando
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.db import transaction


import os


from ..Estudiante.models import Estudiante, Progreso  
from .models import Docente, Curso

from Applications.Caso_Clinico.models import Caso_clinico, Partes_cuerpo, Etapa

from django.shortcuts import redirect

class LoginRequeridoDocenteMixin(View):
    login_url = '/docente/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('usuario_tipo') != 'docente' or not request.session.get('usuario_id'):
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
# -----------------------------------------------------------
# LOGIN DOCENTE
# -----------------------------------------------------------
class Login(TemplateView):
    template_name = 'login/login.html'


# -----------------------------------------------------------
# HOME DOCENTE (PROTEGIDO POR SESIÓN)
# -----------------------------------------------------------
class Home_docente(TemplateView):
    template_name = 'docente/home_docente.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('usuario_tipo') != 'docente':
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        docente_id = self.request.session.get('usuario_id')
        docente = get_object_or_404(Docente, id=docente_id)

        context['docente'] = docente
        context['cursos'] = Curso.objects.filter(curso_docente=docente)

        return context


# ----------------------------------------
# VISTA PARA DETALLE Y PROGRESO
# ----------------------------------------

# ESTA FUNCIÓN FALTANTE DEBE ESTAR FUERA DE CUALQUIER CLASE.
def detalle_curso(request, id):
    # Lógica para obtener el curso
    curso = get_object_or_404(Curso, id=id) 
    contexto = {'curso': curso}
    return render(request, 'docente/detalle_curso.html', contexto)


class ProgresoDocenteView(LoginRequeridoDocenteMixin, TemplateView):
    template_name = 'docente/progreso_docente.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('curso_id')
        
        docente_id = self.request.session.get('usuario_id')
        if docente_id:
            try:
                docente = Docente.objects.get(id=docente_id)
                context['cursos'] = Curso.objects.filter(curso_docente=docente)
                
                if curso_id:
                    curso_seleccionado = get_object_or_404(Curso, id=curso_id, curso_docente=docente)
                    context['curso_seleccionado'] = curso_seleccionado
                    
                    # Obtener estudiantes del curso (si vas a ocupar este codigo, hay que borrar el de abajo, el que dice "este", pero lo ideal seria trabajar con el otro)
                    #estudiantes_curso = Estudiante.objects.filter(
                    #    curso_estudiante=curso_seleccionado
                    #).order_by('apellido_estudiante', 'nombre_estudiante')

                    # Obtener TODOS los estudiantes (mostrar en todos los cursos) (este)
                    estudiantes_curso = Estudiante.objects.all().order_by('apellido_estudiante', 'nombre_estudiante')
                    
                    # Obtener casos clínicos del curso
                    casos_clinicos = Caso_clinico.objects.filter(Curso=curso_seleccionado)
                    
                    progreso_data = []
                    for estudiante in estudiantes_curso:
                        progreso_casos = []
                        total_videos_curso = 0
                        total_vistos_estudiante = 0
                        
                        for caso in casos_clinicos:
                            partes_cuerpo = Partes_cuerpo.objects.filter(CasoClinico=caso)
                            
                            progreso_caso = {
                                'caso': caso,
                                'partes_cuerpo': []
                            }
                            
                            for parte in partes_cuerpo:
                                etapas = Etapa.objects.filter(ParteCuerpo=parte)
                                total_videos_parte = etapas.count()
                                total_videos_curso += total_videos_parte
                                
                                if total_videos_parte > 0:
                                    videos_vistos = Progreso.objects.filter(
                                        progreso_estudiante=estudiante,
                                        progreso_curso=curso_seleccionado,
                                        parte_cuerpo=parte,
                                        video_visto=True
                                    ).count()
                                    
                                    total_vistos_estudiante += videos_vistos
                                    porcentaje = (videos_vistos / total_videos_parte) * 100
                                    
                                    # COLORES MEJORADOS: Rojo < 70% Amarillo >= 70% Verde
                                    if porcentaje == 0:
                                        color = 'danger'  # Rojo
                                    elif porcentaje < 70:
                                        color = 'warning' # Amarillo
                                    else:
                                        color = 'success' # Verde
                                    
                                    progreso_caso['partes_cuerpo'].append({
                                        'parte': parte,
                                        'total_videos': total_videos_parte,
                                        'videos_vistos': videos_vistos,
                                        'porcentaje': round(porcentaje, 1),
                                        'color': color
                                    })
                            
                            progreso_casos.append(progreso_caso)
                        
                        # PROGRESO GENERAL MEJORADO - basado en videos reales
                        if total_videos_curso > 0:
                            progreso_promedio = (total_vistos_estudiante / total_videos_curso) * 100
                        else:
                            progreso_promedio = 0
                        
                        # COLOR DEL PROGRESO GENERAL
                        if progreso_promedio == 0:
                            color_general = 'danger'
                        elif progreso_promedio < 70:
                            color_general = 'warning'
                        else:
                            color_general = 'success'
                        
                        progreso_data.append({
                            'estudiante': estudiante,
                            'progreso_promedio': round(progreso_promedio, 1),
                            'color_general': color_general,
                            'total_videos_curso': total_videos_curso,
                            'total_vistos_estudiante': total_vistos_estudiante,
                            'progreso_casos': progreso_casos
                        })
                    
                    context['progreso_estudiantes'] = progreso_data
                    context['casos_clinicos'] = casos_clinicos
                    
            except Docente.DoesNotExist:
                pass
        
        return context
    
    

# -----------------------------------------------------------
# PERFIL DOCENTE
# -----------------------------------------------------------
class PerfilDocente(TemplateView):
    template_name = 'docente/perfil_docente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_id = self.request.session.get('usuario_id')
        docente = get_object_or_404(Docente, id=docente_id)
        context['docente'] = docente
        context['cursos'] = Curso.objects.filter(curso_docente=docente)
        return context


# -----------------------------------------------------------
# SUBIR FOTO DOCENTE
# -----------------------------------------------------------
def subir_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            docente.foto_perfil_docente = foto
            try:
                # Validar solo la imagen
                docente.foto_perfil_docente.field.clean(foto, docente)
                docente.save()
                messages.success(request, 'Foto actualizada correctamente.')
            except ValidationError as e:
                messages.error(request, e.messages[0])

    return redirect('docente:perfil_docente')


# -----------------------------------------------------------
# ELIMINAR FOTO DOCENTE
# -----------------------------------------------------------
def eliminar_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if docente.foto_perfil_docente:
        if os.path.isfile(docente.foto_perfil_docente.path):
            os.remove(docente.foto_perfil_docente.path)
        docente.foto_perfil_docente = None
        docente.save()
        messages.success(request, 'Foto eliminada correctamente.')

    return redirect('docente:perfil_docente')


# -----------------------------------------------------------
# REGISTRO DOCENTE
# -----------------------------------------------------------

User = get_user_model()

class RegistroDocente(View):
    template_name = 'login/login.html'
    success_url_name = 'login'

    def post(self, request):
        nombre = request.POST.get('nombre_doc')
        apellido = request.POST.get('apellido_doc')
        asignatura = request.POST.get('asigna_doc')
        pais = request.POST.get('pais_doc')
        correo = request.POST.get('correo_doc')
        password = request.POST.get('password_doc')

        if not all([nombre, apellido, correo, password]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, self.template_name)

        dominios_permitidos = ('@gmail.com', '@hotmail.com', '@ucn.cl', '@ce.ucn.cl')
        if not any(correo.endswith(d) for d in dominios_permitidos):
            messages.error(request, f"El correo debe pertenecer a uno de estos dominios: {dominios_permitidos}")
            return render(request, self.template_name)
        
        try:
            with transaction.atomic():
                
                # Crear el objeto User de Django (is_staff=True)
                user_django = User.objects.create_user(
                    username=correo,
                    email=correo,
                    password=password,
                    first_name=nombre,
                    last_name=apellido,
                    is_staff=True # Le da acceso al panel /admin/
                )

            Docente.objects.create(
                user=user_django,
                nombre_docente=nombre,
                apellido_docente=apellido,
                asignatura_docente=asignatura,
                pais_docente=pais
            )

            try:
                # Buscamos el grupo por su nombre
                docente_group = Group.objects.get(name='Docentes')
                
                # Asignamos el usuario recién creado al grupo
                user_django.groups.add(docente_group) 
                
            except Group.DoesNotExist:
                # Si el grupo no existe (por ejemplo, en un entorno de desarrollo nuevo)
                # Simplemente lo reportamos pero permitimos que el registro continúe.
                print("ADVERTENCIA: El grupo 'Docentes' no existe. Créalo en el Admin.")
            
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect(self.success_url_name)

        except IntegrityError:
            messages.error(request, "Este correo ya está registrado.")
            return render(request, self.template_name)


# -----------------------------------------------------------
# AUTENTICAR USUARIO (ESTUDIANTE O DOCENTE)
# -----------------------------------------------------------

class AutenticarUsuario(View):
    template_name = 'login/login.html'

    def post(self, request):
        correo = request.POST.get('correo')
        password = request.POST.get('contrasena')

        # Verificar estudiante
        estudiante = Estudiante.objects.filter(correo_estudiante=correo).first()
        if estudiante and check_password(password, estudiante.contrasena_estudiante):
            request.session['usuario_tipo'] = 'estudiante'
            request.session['usuario_id'] = estudiante.id
            return redirect('estudiante:home_estudiante')

        # Verificar docente
        user_django = authenticate(request, username=correo, password=password)
        if user_django is not None:
            try:
                docente = Docente.objects.get(user=user_django)
                
                # Inicia la sesión de Django
                login(request, user_django) 
                
                request.session['usuario_tipo'] = 'docente'
                request.session['usuario_id'] = docente.pk 
                
                return redirect('docente:home_docente')
            except Docente.DoesNotExist:
                pass
        #Código anterior (por si acaso)
        #docente = Docente.objects.filter(correo_docente=correo).first()
        #if docente and check_password(password, docente.contrasena_docente):
            #request.session['usuario_tipo'] = 'docente'
            #request.session['usuario_id'] = docente.id
            #return redirect('docente:home_docente')

        messages.error(request, "Correo o contraseña incorrectos.")
        return render(request, self.template_name)


# -----------------------------------------------------------
# CERRAR SESIÓN
# -----------------------------------------------------------
class CerrarSesion(View):
    def get(self, request):
        request.session.flush()
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect('login')


# -----------------------------------------------------------
# PÁGINA PRINCIPAL DE CURSOS
# -----------------------------------------------------------

def pagina_principal_docente(request, curso_id):

    curso = get_object_or_404(Curso, pk=curso_id)

    contexto = {
        'curso_actual': curso 
    }

    return render(request, 'docente/docente_pagina_principal.html', contexto)


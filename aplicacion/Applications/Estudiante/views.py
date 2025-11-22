from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import os

from ..Docente.models import Curso
from .models import Estudiante, Progreso
from Applications.Caso_Clinico.models import Caso_clinico, Etapa 


# -----------------------------------------------------------
# HOME ESTUDIANTE (PROTEGIDO POR SESIÓN)
# -----------------------------------------------------------
class Home_estudiante(TemplateView):
    template_name = 'estudiante/home_estudiante.html'

    def get(self, request, *args, **kwargs):
        # Bloquea acceso si no está logueado
        if request.session.get('usuario_tipo') != 'estudiante':
            return redirect('login')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        estudiante_id = self.request.session.get('usuario_id')
        if estudiante_id:
            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                context['estudiante'] = estudiante
                
                # VERIFICACIÓN MEJORADA DE VIDEOS
                if estudiante.curso_estudiante:
                    # Verificar videos por curso específico del estudiante
                    total_videos = Etapa.objects.filter(
                        ParteCuerpo__CasoClinico__Curso=estudiante.curso_estudiante
                    ).count()
                    
                    # DEBUG: Log para verificar
                    print(f"DEBUG - Estudiante: {estudiante.nombre_estudiante}")
                    print(f"DEBUG - Curso: {estudiante.curso_estudiante}")
                    print(f"DEBUG - Total videos: {total_videos}")
                    
                    context['tiene_videos'] = total_videos > 0
                    context['total_videos'] = total_videos
                    context['curso_actual'] = estudiante.curso_estudiante
                else:
                    context['tiene_videos'] = False
                    context['total_videos'] = 0
                    print("DEBUG - Estudiante sin curso asignado")
                    
            except Estudiante.DoesNotExist:
                context['tiene_videos'] = False
                context['total_videos'] = 0
                print("DEBUG - Estudiante no encontrado")
                
        context['cursos'] = Curso.objects.all()
        return context

class CerrarSesion(View):
    def get(self, request):
        request.session.flush() 
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect('login')

# -----------------------------------------------------------
# PERFIL ESTUDIANTE
# -----------------------------------------------------------
class Perfil_estudiante(TemplateView):
    template_name = 'estudiante/perfil_estudiante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        estudiante_id = self.request.session.get('usuario_id')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        context['estudiante'] = estudiante

        progreso_obj = Progreso.objects.filter(progreso_estudiante=estudiante).first()
        context['progreso'] = progreso_obj.porcentaje_progreso if progreso_obj else None

        return context


# -----------------------------------------------------------
# SUBIR FOTO
# -----------------------------------------------------------
def subir_foto_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            estudiante.foto_perfil_estudiante = foto
            try:
                # Validar solo la imagen
                estudiante.foto_perfil_estudiante.field.clean(foto, estudiante)
                estudiante.save()
                messages.success(request, 'Foto actualizada correctamente.')
            except ValidationError as e:
                messages.error(request, e.messages[0])

    return redirect('estudiante:perfil_estudiante')


# -----------------------------------------------------------
# ELIMINAR FOTO
# -----------------------------------------------------------
def eliminar_foto_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if estudiante.foto_perfil_estudiante:
        if os.path.isfile(estudiante.foto_perfil_estudiante.path):
            os.remove(estudiante.foto_perfil_estudiante.path)

        estudiante.foto_perfil_estudiante = None
        estudiante.save()
        messages.success(request, "Foto eliminada correctamente.")

    return redirect('estudiante:perfil_estudiante')


# -----------------------------------------------------------
# REGISTRO ESTUDIANTE
# -----------------------------------------------------------
class RegistroEstudiante(View):
    template_name = 'login/login.html'
    success_url_name = 'login'

    def post(self, request):
        nombre = request.POST.get('nombre_est')
        apellido = request.POST.get('apellido_est')
        pais = request.POST.get('pais_est')
        correo = request.POST.get('correo_est')
        password = request.POST.get('password_est')

        # Validaciones
        if not all([nombre, apellido, pais, correo, password]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, self.template_name)

        if not correo.endswith('@alumnos.ucn.cl'):
            messages.error(request, "El correo debe terminar en @alumnos.ucn.cl.")
            return render(request, self.template_name)
        
         # VERIFICAR SI EL CORREO YA EXISTE
        if Estudiante.objects.filter(correo_estudiante=correo).exists():
            messages.error(request, f"El correo {correo} ya está registrado.")
            return render(request, self.template_name)

        try:
            hashed_password = make_password(password)

           # CREAR ESTUDIANTE SIN curso_estudiante_id fijo
            Estudiante.objects.create(
                nombre_estudiante=nombre,
                apellido_estudiante=apellido,
                pais_estudiante=pais,
                correo_estudiante=correo,
                contrasena_estudiante=hashed_password,
                #curso_estudiante_id=2,
                foto_perfil_estudiante=None
            )

            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect(self.success_url_name)
        
        except Exception as e:
            messages.error(request, f"Error en el registro: {str(e)}")
            return render(request, self.template_name)

       # except IntegrityError:
        #    messages.error(request, "Este correo ya está registrado.")
        #    return render(request, self.template_name)


# -----------------------------------------------------------
# LOGIN
# -----------------------------------------------------------
def login_estudiante(request):
    return render(request, 'estudiante/login.html')


# -----------------------------------------------------------
# AUTENTICAR
# -----------------------------------------------------------
def autenticar_estudiante(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        estudiante = Estudiante.objects.filter(correo_estudiante=correo).first()

        if not estudiante or not check_password(contrasena, estudiante.contrasena_estudiante):
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('estudiante:login')

        # Crear sesión
        request.session['usuario_tipo'] = 'estudiante'
        request.session['usuario_id'] = estudiante.id

        return redirect('estudiante:home_estudiante')

    return redirect('estudiante:login')


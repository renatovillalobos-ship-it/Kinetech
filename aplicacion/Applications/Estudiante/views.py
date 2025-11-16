from django.shortcuts import render , redirect
from ..Docente.models import Curso
from .models import Estudiante, Progreso
from django.contrib.auth.hashers import make_password, check_password
import os
from django.db import IntegrityError
from django.views import View

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect


# Create your views here.
from django.views.generic import (
    TemplateView,


)


import os
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

class Home_estudiante(TemplateView):
    template_name='estudiante/home_estudiante.html'

    def get_context_data(self, **kwargs):
        cursosbd = super().get_context_data(**kwargs)
        cursosbd['cursos']=Curso.objects.all()
        return cursosbd
    

class Perfil_estudiante(TemplateView):
    template_name = 'estudiante/perfil_estudiante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Tomar el PRIMER estudiante temporalmente (para pruebas sin login)
        estudiante = Estudiante.objects.first()   
        context['estudiante'] = estudiante


        # ---------------------------------------------
        # OBTENER EL PROGRESO REAL DESDE LA TABLA PROGRESO
        # ---------------------------------------------
        progreso_obj = Progreso.objects.filter(progreso_estudiante=estudiante).first()

        context['progreso'] = progreso_obj.porcentaje_progreso if progreso_obj else None

        return context
    

# -----------------------------------------------------------------------
def subir_foto_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            estudiante.foto_perfil_estudiante = foto
            estudiante.save()
            messages.success(request, "Foto actualizada correctamente.")

    return redirect('estudiante:perfil_estudiante')


def eliminar_foto_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if estudiante.foto_perfil_estudiante:
        if os.path.isfile(estudiante.foto_perfil_estudiante.path):
            os.remove(estudiante.foto_perfil_estudiante.path)

        estudiante.foto_perfil_estudiante = None
        estudiante.save()
        messages.success(request, "Foto eliminada correctamente.")

    return redirect('estudiante:perfil_estudiante')

class RegistroEstudiante(View):
    template_name = 'login/login.html'
    success_url_name = 'login' # Nombre de la URL de inicio de sesión



    def post(self, request):
        # 1. Obtener datos (ya NO se busca 'carrera_estudiante')
        nombre_estudiante = request.POST.get('nombre_est')
        apellido_estudiante = request.POST.get('apellido_est')
        pais_estudiante = request.POST.get('pais_est')
        correo_estudiante = request.POST.get('correo_est')
        contrasena_estudiante = request.POST.get('password_est')
        
       
        # 2. Validación de campos obligatorios
        if not all([nombre_estudiante, apellido_estudiante, correo_estudiante, contrasena_estudiante]):
            messages.error(request, "Todos los campos del estudiante son obligatorios.")
            return render(request, self.template_name)
       
        # 3. Validación de Correo: Solo @alumnos.ucn.cl (ESTRICTA)
        dominio_institucional = '@alumnos.ucn.cl'



        if not correo_estudiante.endswith(dominio_institucional):
            messages.error(request, f"El correo debe ser institucional y terminar en {dominio_institucional}. Por favor vuelva a intentar.")
            return render(request, self.template_name)
           
        try:
            # 4. CIFRAR LA CONTRASEÑA y crear el Estudiante
            hashed_password = make_password(contrasena_estudiante)
           
            Estudiante.objects.create(
                nombre_estudiante=nombre_estudiante, 
                apellido_estudiante=apellido_estudiante,
                pais_estudiante=pais_estudiante,
                correo_estudiante=correo_estudiante,
                contrasena_estudiante=hashed_password,
                curso_estudiante_id = 2,
                foto_perfil_estudiante=None
                # NOTA: Si el campo 'carrera_estudiante' existía y no tiene un default,
                # debes eliminarlo del models.py o asignarle un valor fijo aquí (ej: 'Kinesiología').
            )



            messages.success(request, "¡Registro de estudiante exitoso! Ahora puedes iniciar sesión.")
           
            # 5. Redirigir al login
            return redirect(self.success_url_name)



        except IntegrityError:
             messages.error(request, "El correo electrónico ya se encuentra registrado. Ve al apartado de iniciar sesión.")
             return render(request, self.template_name)
        except Exception as e:
             messages.error(request, f"Error al registrar. Intente nuevamente.")
             return render(request, self.template_name)
        


class HomeEstudiante(View):
    def get(self, request):
        if request.session.get('usuario_tipo') == 'estudiante':
            return render(request, 'estudiante/home_estudiante.html') 
        return redirect('login')






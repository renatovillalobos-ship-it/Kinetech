from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from Applications.Estudiante.models import Estudiante, Progreso
from django.db.models import Avg



# Create your views here.
from django.views.generic import (
    TemplateView,

)

from .models import Docente, Curso 

import os


class Login(TemplateView):
    template_name = 'login/login.html'

class Home_docente(TemplateView):
    template_name = 'docente/home_docente.html'
    def get_context_data(self, **kwargs):
        cursosbd = super().get_context_data(**kwargs)
        cursosbd['cursos']=Curso.objects.all()
        return cursosbd

# ----------------------------------------
# VISTA PARA DETALLE Y PROGRESO
# ----------------------------------------

# ESTA FUNCIÓN FALTANTE DEBE ESTAR FUERA DE CUALQUIER CLASE.
def detalle_curso(request, id):
    # Lógica para obtener el curso
    curso = get_object_or_404(Curso, id=id) 
    contexto = {'curso': curso}
    return render(request, 'docente/detalle_curso.html', contexto)


class ProgresoDocenteView(LoginRequiredMixin, TemplateView):
    template_name = 'docente/progreso_docente.html'
    
    # Solo un bloque de get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = kwargs.get('curso_id')
        
        docente = self.request.user.docente # Asume que el docente existe por LoginRequiredMixin
        context['cursos'] = Curso.objects.filter(docente=docente)
        
        if curso_id:
            context['curso_seleccionado'] = get_object_or_404(Curso, id=curso_id)
        
        return context


# ----------------------------------------
# VISTAS DE PERFIL Y FOTO
# ----------------------------------------

class PerfilDocente(TemplateView):
    template_name = 'docente/perfil_docente.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Idealmente, usa self.request.user.docente
        context['docente'] = Docente.objects.first()
        return context
    
    
def subir_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            docente.foto_perfil_docente = foto
            docente.save()
            messages.success(request, 'Foto actualizada correctamente.')

    return redirect('docente:perfil_docente')


def eliminar_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if docente.foto_perfil_docente:
        # Eliminar archivo físico
        if os.path.isfile(docente.foto_perfil_docente.path):
            os.remove(docente.foto_perfil_docente.path)
        docente.foto_perfil_docente = None
        docente.save()
        messages.success(request, 'Foto eliminada correctamente.')

    return redirect('docente:perfil_docente')

class RegistroDocente(View):
    template_name = 'login/login.html' # Asumiendo que esta es la ruta a tu plantilla
    success_url_name = 'login' # La URL de la vista de inicio de sesión



    def post(self, request):
        # 1. Obtener datos
        nombre_docente = request.POST.get('nombre_doc')
        apellido_docente  = request.POST.get('apellido_doc')
        asignatura_docente = request.POST.get('asigna_doc')
        pais_docente = request.POST.get('pais_doc')
        correo_docente = request.POST.get('correo_doc')
        contrasena_docente  = request.POST.get('password_doc')
       
        # Validación de campos obligatorios
        if not all([nombre_docente, apellido_docente, correo_docente, contrasena_docente]):
            messages.error(request, "Todos los campos del docente son obligatorios.")
            return render(request, self.template_name)



        # Validación de Correo: Dominios Flexibles
        dominios_permitidos = ('@gmail.com', '@hotmail.com', '@ucn.cl', '@ce.ucn.cl')
        es_valido = any(correo_docente.endswith(d) for d in dominios_permitidos)
       
        if not es_valido:
            messages.error(request, f"El correo debe pertenecer a los siguientes dominios: {dominios_permitidos}. Por favor vuelva a intentar.")
            return render(request, self.template_name)
           
        try:
            # 2. CIFRAR LA CONTRASEÑA y crear el Docente
            hashed_password = make_password(contrasena_docente)



            Docente.objects.create(
                nombre_docente=nombre_docente,
                apellido_docente=apellido_docente,
                asignatura_docente = asignatura_docente,
                pais_docente=pais_docente,
                correo_docente=correo_docente,
                contrasena_docente=hashed_password,
            )



            messages.success(request, "¡Registro de docente exitoso! Ahora puedes iniciar sesión.")
            return redirect(self.success_url_name)



        except IntegrityError:
             messages.error(request, "El correo electrónico ya se encuentra registrado. Ve al apartado de iniciar sesión.")
             return render(request, self.template_name)
        except Exception as e:
             messages.error(request, f"Error al registrar. Intente nuevamente.")
             return render(request, self.template_name)

class AutenticarUsuario(View):
    template_name = 'login/login.html'

    def post(self, request):
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        
        # 1. Buscar y validar Estudiante
        estudiante = Estudiante.objects.filter(correo_estudiante=correo).first()
        if estudiante and check_password(contrasena, estudiante.contrasena_estudiante):
            request.session['usuario_tipo'] = 'estudiante'
            request.session['usuario_id'] = estudiante.id
            # Redirige a la URL completa
            return redirect('estudiante:home_estudiante') 
            
        # 2. Buscar y validar Docente
        docente = Docente.objects.filter(correo_docente=correo).first()
        if docente and check_password(contrasena, docente.contrasena_docente):
            request.session['usuario_tipo'] = 'docente'
            request.session['usuario_id'] = docente.id
            #Redirige a la URL completa 
            return redirect('docente:home_docente')
            
        # 3. Fallo
        messages.error(request, "Credenciales incorrectas.")
        return render(request, self.template_name)

class CerrarSesion(View):
    def get(self, request):
        request.session.flush() 
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect('login')
    
class HomeDocente(View):
    def get(self, request):
        if request.session.get('usuario_tipo') == 'docente':
            return render(request, 'docente/home_docente.html')
        return redirect('login')


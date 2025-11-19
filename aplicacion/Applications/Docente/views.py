from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
import os

from ..Estudiante.models import Estudiante
from .models import Docente, Curso


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
        # Bloquea acceso si no está logueado
        if request.session.get('usuario_tipo') != 'docente':
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Curso.objects.all()
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
            docente.save()
            messages.success(request, 'Foto actualizada correctamente.')

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
            hashed_password = make_password(password)
            Docente.objects.create(
                nombre_docente=nombre,
                apellido_docente=apellido,
                asignatura_docente=asignatura,
                pais_docente=pais,
                correo_docente=correo,
                contrasena_docente=hashed_password
            )
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
        docente = Docente.objects.filter(correo_docente=correo).first()
        if docente and check_password(password, docente.contrasena_docente):
            request.session['usuario_tipo'] = 'docente'
            request.session['usuario_id'] = docente.id
            return redirect('docente:home_docente')

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

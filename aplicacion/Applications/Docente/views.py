from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages

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
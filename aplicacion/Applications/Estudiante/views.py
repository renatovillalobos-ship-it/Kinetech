from django.shortcuts import render
from ..Docente.models import Curso
from .models import Estudiante, Progreso
import os
from django.contrib import messages
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

        # Obtener el primer estudiante (o el único)
        estudiante = Estudiante.objects.filter(
            correo_estudiante=self.request.user.email
        ).first()

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




from django.shortcuts import render
from ..Docente.models import Curso

# Create your views here.
from django.views.generic import (
    TemplateView,


)

class Home_estudiante(TemplateView):
    template_name='estudiante/home_estudiante.html'

    def get_context_data(self, **kwargs):
        cursosbd = super().get_context_data(**kwargs)
        cursosbd['cursos']=Curso.objects.all()
        return cursosbd
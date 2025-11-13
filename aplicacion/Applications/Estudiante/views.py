from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    TemplateView,


)

class Home_estudiante(TemplateView):
    template_name='estudiante/home_estudiante.html'
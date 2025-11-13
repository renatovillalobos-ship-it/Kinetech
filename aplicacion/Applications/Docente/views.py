from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    TemplateView,


)

class Login(TemplateView):
    template_name='login/login.html'

class Home_docente(TemplateView):
    template_name='docente/home_docente.html'
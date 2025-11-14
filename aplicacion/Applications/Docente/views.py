from django.shortcuts import render
from .models import Curso 
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.views.generic import (
    TemplateView,


)

class Login(TemplateView):
    template_name='login/login.html'

class Home_docente(TemplateView):
    template_name='docente/home_docente.html'

@login_required 
def inicio_docente(request):

    try:
        docente_actual = request.user.docente
    except:

        return render(request, 'error_no_docente.html')

    cursos_del_docente = Curso.objects.filter(docente=docente_actual)

    contexto = {
        'cursos': cursos_del_docente,
    }
    
    return render(request, 'inicio_docente.html', contexto)
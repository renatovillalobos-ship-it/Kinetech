from django.shortcuts import render
from .models import Curso 
from django.contrib.auth.decorators import login_required
from .models import Docente

# Create your views here.
from django.views.generic import (
    TemplateView,


)

import os
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect



class Login(TemplateView):
    template_name='login/login.html'

class Home_docente(TemplateView):
    template_name='docente/home_docente.html'


#gregue lo que esta abajo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Tomar el PRIMER docente (o el único existente)
        context['docente'] = Docente.objects.first()

        return context
    
# 1. VISTA NECESARIA PARA MOSTRAR TU PERFIL
class PerfilDocente(TemplateView):
    template_name='docente/perfil_docente.html' # Asegúrate de la ruta   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['docente'] = Docente.objects.first()  # o el docente logueado
        return context
    
    #ESTO PARA LA FOTO
    
def subir_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            docente.foto_perfil_docente = foto
            docente.save()
            messages.success(request, 'Foto actualizada correctamente.')

    return redirect('perfil_docente')


def eliminar_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if docente.foto_perfil_docente:
            # Eliminar archivo físico
        if os.path.isfile(docente.foto_perfil_docente.path):
            os.remove(docente.foto_perfil_docente.path)
        docente.foto_perfil_docente = None
        docente.save()
        messages.success(request, 'Foto eliminada correctamente.')

    return redirect('perfil_docente')

#Para el tema de los cursos

def detalle_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'docente/detalle_curso.html', {'curso': curso})



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
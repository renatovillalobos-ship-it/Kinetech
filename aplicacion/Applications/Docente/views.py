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


from Applications.Estudiante.models import Estudiante, Progreso
from django.db.models import Avg


class Login(TemplateView):
    template_name='login/login.html'

class Home_docente(TemplateView):
    template_name='docente/home_docente.html'


#gregue lo que esta abajo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Tomar el PRIMER docente (o el único existente)
        docente = Docente.objects.first()
        context['docente'] = docente
        
        # AÑADIR: Pasar cursos al contexto
        if docente:
            context['cursos'] = Curso.objects.filter(curso_docente=docente)
        else:
            context['cursos'] = []

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




class ProgresoDocenteView(TemplateView):
    """Vista para mostrar el progreso de estudiantes - Basada en TemplateView"""
    template_name = 'docente/progreso_docente.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el docente (usando la misma lógica que en Home_docente)
        docente = Docente.objects.first()
        context['docente'] = docente
        
        # Obtener todos los cursos del docente
        cursos_docente = Curso.objects.filter(curso_docente=docente)
        context['cursos'] = cursos_docente
        
        # Verificar si hay un curso_id en los parámetros de la URL
        curso_id = self.kwargs.get('curso_id')
        
        if curso_id:
            # Obtener el curso específico seleccionado
            curso_seleccionado = get_object_or_404(Curso, id=curso_id, curso_docente=docente)
            context['curso_seleccionado'] = curso_seleccionado
            
            # Obtener estudiantes del curso ordenados alfabéticamente por apellido
            estudiantes_curso = Estudiante.objects.filter(
                curso_estudiante=curso_seleccionado
            ).order_by('apellido_estudiante', 'nombre_estudiante')
            
            # Preparar datos de progreso para cada estudiante
            progreso_estudiantes = []
            for estudiante in estudiantes_curso:
                # Obtener todos los progresos del estudiante en este curso
                progresos = Progreso.objects.filter(
                    progreso_estudiante=estudiante,
                    progreso_curso=curso_seleccionado
                )
                
                # Calcular progreso promedio
                progreso_promedio = progresos.aggregate(
                    promedio=Avg('porcentaje_progreso')
                )['promedio'] or 0
                
                progreso_estudiantes.append({
                    'estudiante': estudiante,
                    'progresos': progresos,
                    'progreso_promedio': round(float(progreso_promedio), 1)
                })
            
            context['progreso_estudiantes'] = progreso_estudiantes
        
        return context
    
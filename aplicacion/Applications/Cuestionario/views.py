from django.shortcuts import render, get_object_or_404, redirect
from .models import cuestionario as CuestionarioModelo, Preguntas, Respuesta
from Applications.Docente.models import Curso
from django.shortcuts import redirect

def ver_cuestionario(request, curso_id, cuestionario_id=None):
    curso = get_object_or_404(Curso, id=curso_id)
    
    if not cuestionario_id:
        cuestionarios = CuestionarioModelo.objects.filter(Curso=curso)
        if cuestionarios.exists():
            cuestionario = cuestionarios.first()
            return redirect('cuestionario:cuestionario_detalle', curso_id=curso_id, cuestionario_id=cuestionario.id)
    
    cuestionario = get_object_or_404(CuestionarioModelo, id=cuestionario_id, Curso=curso)
    preguntas = Preguntas.objects.filter(cuestionario=cuestionario).prefetch_related('respuesta_set')
    
    cuestionarios_todos = CuestionarioModelo.objects.filter(Curso=curso)
    cuestionarios_iniciales = cuestionarios_todos.filter(nombre='Inicial')
    cuestionarios_finales = cuestionarios_todos.filter(nombre='Final')
    
    if request.method == 'POST':
        respuestas_seleccionadas = {}
        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_id:
                respuestas_seleccionadas[pregunta.id] = int(respuesta_id)

        puntaje = 0
        for pregunta in preguntas:
            selected_id = respuestas_seleccionadas.get(pregunta.id)
            if selected_id:
                correcta = Respuesta.objects.get(id=selected_id).es_correcta
                if correcta:
                    puntaje += 1

        return render(request, 'estudiante/cuestionario_resultado.html', {
            'curso_actual': curso,
            'puntaje': puntaje,
            'total': preguntas.count(),
            'cuestionario_actual': cuestionario,
            'cuestionarios_iniciales': cuestionarios_iniciales,
            'cuestionarios_finales': cuestionarios_finales
        })

    context = {
        'curso_actual': curso,
        'preguntas': preguntas,
        'cuestionario_actual': cuestionario,
        'cuestionarios_iniciales': cuestionarios_iniciales,
        'cuestionarios_finales': cuestionarios_finales,
        'cuestionario_id': cuestionario.id
    }
    return render(request, 'estudiante/cuestionario.html', context)

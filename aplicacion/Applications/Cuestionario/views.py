from django.shortcuts import render, get_object_or_404, redirect
from .models import cuestionario as CuestionarioModelo, Preguntas, Respuesta
from Applications.Docente.models import Curso

def ver_cuestionario(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Tomar el primer cuestionario del curso
    cuestionarios = CuestionarioModelo.objects.filter(Curso=curso)
    if not cuestionarios.exists():
        return render(request, 'estudiante/cuestionario.html', {
            'curso_actual': curso,
            'preguntas': []
        })

    cuestionario = cuestionarios.first()
    preguntas = Preguntas.objects.filter(cuestionario=cuestionario).prefetch_related('respuesta_set')

    if request.method == 'POST':
        respuestas_seleccionadas = {}
        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_id:
                respuestas_seleccionadas[pregunta.id] = int(respuesta_id)

        # Calcular puntaje
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
            'total': preguntas.count()
        })

    context = {
        'curso_actual': curso,
        'preguntas': preguntas
    }
    return render(request, 'estudiante/cuestionario.html', context)

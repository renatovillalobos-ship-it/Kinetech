from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from Applications.Estudiante.models import (
    Estudiante, Progreso, RespuestaEstudiante, ResultadoCuestionario
)
from Applications.Cuestionario.models import cuestionario, Preguntas, Respuesta
from Applications.Docente.models import Curso
from django.urls import reverse


# -------------------------------------------
# Función para traer preguntas de un cuestionario
# -------------------------------------------
def obtener_preguntas(cuest_id):
    preguntas = Preguntas.objects.filter(cuestionario_id=cuest_id).prefetch_related("respuesta_set")
    return preguntas


# -------------------------------------------
# AJAX: INSTRUCCIONES
# -------------------------------------------
def ajax_instrucciones(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, "estudiante/ajax/instrucciones.html", {
        "curso_actual": curso
    })


# -------------------------------------------
# AJAX: CUESTIONARIO
# -------------------------------------------
def ajax_cuestionario(request, curso_id, cuest_id):
    preguntas = obtener_preguntas(cuest_id)
    return render(request, "estudiante/ajax/cuestionario.html", {
        "preguntas": preguntas,
        "cuestionario_id": cuest_id,
        "curso_id": curso_id,
    })



# -------------------------------------------
# AJAX: CASO CLÍNICO
# -------------------------------------------
def ajax_caso_clinico(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, "estudiante/ajax/caso_clinico.html", {
        "curso_actual": curso
    })


# -------------------------------------------
# AJAX: EVALUACIONES
# -------------------------------------------
def ajax_evaluaciones(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, "estudiante/ajax/evaluaciones.html", {
        "curso_actual": curso
    })

def curso_panel(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    cuestionarios = cuestionario.objects.filter(Curso=curso)

    # Para saber cuáles cuestionarios ya respondió este estudiante
    estudiante_id = request.session.get("usuario_id")
    cuestionarios_respondidos = []

    if estudiante_id:
        estudiante = Estudiante.objects.get(id=estudiante_id)
        cuestionarios_respondidos = list(
            ResultadoCuestionario.objects.filter(
                estudiante=estudiante,
                cuestionario__in=cuestionarios
            ).values_list("cuestionario_id", flat=True)
        )

    url_instrucciones = reverse("estudiante:ajax_instrucciones", args=[curso_id])

    return render(request, 'estudiante/curso.html', {
        'curso_actual': curso,
        'curso_id': curso.id,
        'cuestionarios': cuestionarios,
        'cuestionarios_respondidos': cuestionarios_respondidos,
        'url_instrucciones': url_instrucciones,
    })


def ajax_guardar_respuestas(request, curso_id, cuest_id):

    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    # Obtener estudiante desde la sesión
    estudiante_id = request.session.get("usuario_id")
    if not estudiante_id:
        return JsonResponse({"error": "Estudiante no autenticado"}, status=401)

    estudiante = Estudiante.objects.get(id=estudiante_id)
    curso = Curso.objects.get(id=curso_id)
    cuest = cuestionario.objects.get(id=cuest_id)

    # 🔒 Verificar si ya respondió el cuestionario completo
    if ResultadoCuestionario.objects.filter(estudiante=estudiante, cuestionario=cuest).exists():
        return JsonResponse({
            "ya_respondido": True,
            "mensaje": "Ya respondiste este cuestionario.",
        })

    preguntas = Preguntas.objects.filter(cuestionario=cuest)
    total_preguntas = preguntas.count()
    puntaje_final = 0

    # Guardar respuestas individuales
    for pregunta in preguntas:
        respuesta_id = request.POST.get(f"pregunta_{pregunta.id}")

        if respuesta_id:
            respuesta = Respuesta.objects.get(id=respuesta_id)

            # Registrar respuesta del estudiante (solo una vez por pregunta)
            RespuestaEstudiante.objects.update_or_create(
                estudiante=estudiante,
                pregunta=pregunta,
                cuestionario=cuest,
                defaults={"respuesta": respuesta}
            )

            if respuesta.es_correcta:
                puntaje_final += 1

    porcentaje = (puntaje_final / total_preguntas) * 100 if total_preguntas > 0 else 0

    # Guardar resultado final
    ResultadoCuestionario.objects.create(
        estudiante=estudiante,
        cuestionario=cuest,
        puntaje=puntaje_final,
        porcentaje=porcentaje
    )

    # Registrar un progreso general (opcional)
    Progreso.objects.create(
        fecha_progreso_inicial=timezone.now(),
        fecha_progreso_termino=timezone.now(),
        puntaje_obtenido_inicial=0,
        puntaje_obtenido_final=puntaje_final,
        porcentaje_progreso=porcentaje,
        progreso_curso=curso,
        progreso_estudiante=estudiante,
        docente_Correspondiente_progreso=curso.curso_docente
    )

    return JsonResponse({
        "success": True,
        "mensaje": "Respuestas guardadas correctamente.",
        "puntaje": puntaje_final,
        "porcentaje": porcentaje
    })
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
    
    # Obtener el cuestionario para saber su tipo
    cuestionario_obj = get_object_or_404(cuestionario, id=cuest_id)
    
    # Variables para el diagnóstico
    respuestas_estudiante = {} 
    nivel_diagnostico = None
    porcentaje_correctas = 0
    respuestas_correctas = 0
    total_preguntas = preguntas.count()
    cuestionario_respondido = False

    estudiante_id = request.session.get("usuario_id")
    if estudiante_id:
        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            
            # Verificar si ya respondió este cuestionario
            resultado_existente = ResultadoCuestionario.objects.filter(
                estudiante=estudiante,
                cuestionario=cuestionario_obj
            ).first()
            
            if resultado_existente:
                cuestionario_respondido = True
                
                # Obtener todas las respuestas del estudiante para este cuestionario
                respuestas = RespuestaEstudiante.objects.filter(
                    estudiante=estudiante,
                    pregunta__cuestionario=cuestionario_obj
                ).select_related('respuesta')
                
                # Crear diccionario SIMPLE de respuestas del estudiante
                for respuesta_est in respuestas:
                    # Solo guardamos el ID de la respuesta seleccionada
                    respuestas_estudiante[respuesta_est.pregunta.id] = respuesta_est.respuesta.id
                    
                    if respuesta_est.respuesta.es_correcta:
                        respuestas_correctas += 1
                
                # Calcular porcentaje y nivel
                if total_preguntas > 0:
                    porcentaje_correctas = (respuestas_correctas / total_preguntas) * 100
                    
                    # Determinar nivel según porcentaje
                    if porcentaje_correctas >= 80:
                        nivel_diagnostico = 'alta'
                    elif porcentaje_correctas >= 50:
                        nivel_diagnostico = 'media'
                    else:
                        nivel_diagnostico = 'baja'
                        
        except Estudiante.DoesNotExist:
            pass
    
    curso = get_object_or_404(Curso, id=curso_id)
    cuestionarios_todos = cuestionario.objects.filter(Curso=curso)
    cuestionarios_iniciales = cuestionarios_todos.filter(nombre='Inicial')
    cuestionarios_finales = cuestionarios_todos.filter(nombre='Final')
    
    return render(request, "estudiante/ajax/cuestionario.html", {
        "preguntas": preguntas,
        "cuestionario_id": cuest_id,
        "curso_id": curso_id,
        "cuestionario_actual": cuestionario_obj,
        "cuestionarios_iniciales": cuestionarios_iniciales,
        "cuestionarios_finales": cuestionarios_finales,
        "respuestas_estudiante": respuestas_estudiante, 
        "nivel_diagnostico": nivel_diagnostico,
        "porcentaje_correctas": porcentaje_correctas,
        "respuestas_correctas": respuestas_correctas,
        "total_preguntas": total_preguntas,
        "cuestionario_respondido": cuestionario_respondido,
    })

# -------------------------------------------
# AJAX: CASO CLÍNICO
# -------------------------------------------
def ajax_caso_clinico(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, "estudiante/ajax/caso_clinico.html", {
        "curso_actual": curso
    })

def ajax_guia_kine(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, "estudiante/ajax/guia_kine.html", {
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
    
    # Separar cuestionarios por tipo
    cuestionarios_todos = cuestionario.objects.filter(Curso=curso)
    cuestionarios_iniciales = cuestionarios_todos.filter(nombre='Inicial')
    cuestionarios_finales = cuestionarios_todos.filter(nombre='Final')

    # Para saber cuáles cuestionarios ya respondió este estudiante
    estudiante_id = request.session.get("usuario_id")
    cuestionarios_respondidos = []

    if estudiante_id:
        estudiante = Estudiante.objects.get(id=estudiante_id)
        cuestionarios_respondidos = list(
            ResultadoCuestionario.objects.filter(
                estudiante=estudiante,
                cuestionario__in=cuestionarios_todos
            ).values_list("cuestionario_id", flat=True)
        )

    url_instrucciones = reverse("estudiante:ajax_instrucciones", args=[curso_id])

    return render(request, 'estudiante/curso.html', {
        'curso_actual': curso,
        'curso_id': curso.id,
        'cuestionarios_iniciales': cuestionarios_iniciales,  
        'cuestionarios_finales': cuestionarios_finales,      
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

    if ResultadoCuestionario.objects.filter(estudiante=estudiante, cuestionario=cuest).exists():
        return JsonResponse({
            "ya_respondido": True,
            "mensaje": "Ya respondiste este cuestionario.",
        })

    preguntas = Preguntas.objects.filter(cuestionario=cuest)
    total_preguntas = preguntas.count()
    puntaje_final = 0
    detalle_respuestas = []
    texto_nivel = ""
    texto_recomendacion = ""

    # Guardar respuestas individuales
    for pregunta in preguntas:
        respuesta_id = request.POST.get(f"pregunta_{pregunta.id}")

        if respuesta_id:
            respuesta = Respuesta.objects.get(id=respuesta_id)

            # Registrar respuesta del estudiante
            RespuestaEstudiante.objects.update_or_create(
                estudiante=estudiante,
                pregunta=pregunta,
                cuestionario=cuest,
                defaults={"respuesta": respuesta}
            )

            es_correcta = respuesta.es_correcta
            if es_correcta:
                puntaje_final += 1
            
            detalle_respuestas.append({
                'pregunta_id': pregunta.id,
                'respuesta_id': respuesta_id,
                'es_correcta': es_correcta
            })

    porcentaje = (puntaje_final / total_preguntas) * 100 if total_preguntas > 0 else 0
    
    # Calcular nivel de diagnóstico
    if porcentaje >= 80:
        nivel_diagnostico = 'alta'
    elif porcentaje >= 50:
        nivel_diagnostico = 'media'
    else:
        nivel_diagnostico = 'baja'

    
    if nivel_diagnostico == 'alta':
        texto_nivel = "Alto"
        texto_recomendacion = "¡Excelente!"
    elif nivel_diagnostico == 'media':
        texto_nivel = "Medio"
        texto_recomendacion = "Buen trabajo, pero hay áreas para mejorar."
    elif nivel_diagnostico == 'baja':
        texto_nivel = "Bajo"
        texto_recomendacion = "Te recomendamos revisar los contenidos."

    # Guardar resultado final
    ResultadoCuestionario.objects.create(
        estudiante=estudiante,
        cuestionario=cuest,
        puntaje=puntaje_final,
        porcentaje=porcentaje
    )


    return JsonResponse({
        "success": True,
        "mensaje": "Respuestas guardadas correctamente.",
        "puntaje": puntaje_final,
        "porcentaje": porcentaje,
        "nivel_diagnostico": nivel_diagnostico, 
        "texto_nivel": texto_nivel,         
        "texto_recomendacion": texto_recomendacion,
        "total_preguntas": total_preguntas,
        "detalle_respuestas": detalle_respuestas,
        "respuestas_correctas": puntaje_final,
    })

# -------------------------------------------
# NUEVA: AJAX para cargar sidebar con cuestionarios separados
# -------------------------------------------
def ajax_sidebar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Separar cuestionarios por tipo
    cuestionarios_todos = cuestionario.objects.filter(Curso=curso)
    cuestionarios_iniciales = cuestionarios_todos.filter(nombre='Inicial')
    cuestionarios_finales = cuestionarios_todos.filter(nombre='Final')

    # Para saber cuáles cuestionarios ya respondió este estudiante
    estudiante_id = request.session.get("usuario_id")
    cuestionarios_respondidos = []

    if estudiante_id:
        estudiante = Estudiante.objects.get(id=estudiante_id)
        cuestionarios_respondidos = list(
            ResultadoCuestionario.objects.filter(
                estudiante=estudiante,
                cuestionario__in=cuestionarios_todos
            ).values_list("cuestionario_id", flat=True)
        )

    return render(request, 'estudiante/sidebar_curso.html', {
        'curso_id': curso_id,
        'cuestionarios_iniciales': cuestionarios_iniciales,
        'cuestionarios_finales': cuestionarios_finales,
        'cuestionarios_respondidos': cuestionarios_respondidos,
    })
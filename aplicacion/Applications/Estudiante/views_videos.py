from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Progreso, Estudiante
from Applications.Caso_Clinico.models import Etapa, Partes_cuerpo, Caso_clinico  
from Applications.Docente.models import Curso

def lista_videos_estudiante(request):
    """Vista para que estudiantes vean la lista de videos disponibles"""
    estudiante_id = request.session.get('usuario_id')
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    curso_actual = estudiante.curso_estudiante
    
    if not curso_actual:
        messages.warning(request, "No estás asignado a ningún curso.")
        return render(request, 'estudiante/lista_videos.html', {'videos_data': []})
    
    # Obtener todos los casos clínicos del CURSO ACTUAL del estudiante
    casos_clinicos = Caso_clinico.objects.filter(Curso=curso_actual)
    
    # Estructurar datos para el template
    videos_data = []
    for caso in casos_clinicos:
        partes_cuerpo = Partes_cuerpo.objects.filter(CasoClinico=caso)
        
        for parte in partes_cuerpo:
            etapas = Etapa.objects.filter(ParteCuerpo=parte)
            
            for etapa in etapas:
                # Verificar si el estudiante ya vio este video
                video_visto = Progreso.objects.filter(
                    progreso_estudiante=estudiante,
                    etapa_completada=etapa,
                    video_visto=True
                ).exists()
                
                videos_data.append({
                    'caso': caso,
                    'parte': parte,
                    'etapa': etapa,
                    'video_visto': video_visto
                })
    
    return render(request, 'estudiante/lista_videos.html', {
        'videos_data': videos_data,
        'curso_actual': curso_actual
    })

def ver_video(request, etapa_id):
    """Vista para reproducir un video específico"""
    etapa = get_object_or_404(Etapa, id=etapa_id)
    estudiante_id = request.session.get('usuario_id')  
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)  
    
    # Marcar automáticamente como visto cuando se accede a la página
    marcar_video_como_visto(estudiante, etapa)
    
    return render(request, 'estudiante/ver_video.html', {
        'etapa': etapa,
        'estudiante': estudiante
    })

def marcar_video_como_visto(estudiante, etapa):
    """Función helper para marcar un video como visto"""
    curso_etapa = etapa.ParteCuerpo.CasoClinico.Curso
    docente_curso = curso_etapa.curso_docente
    
    # Verificar si ya existe registro para ESTA ETAPA específica
    if not Progreso.objects.filter(
        progreso_estudiante=estudiante,
        etapa_completada=etapa
    ).exists():
        
        Progreso.objects.create(
            fecha_progreso_inicial=timezone.now().date(),
            fecha_progreso_termino=timezone.now().date(),
            puntaje_obtenido_inicial=0,
            puntaje_obtenido_final=10,
            porcentaje_progreso=100,
            progreso_curso=curso_etapa,  # CURSO DE LA ETAPA, no del estudiante
            progreso_estudiante=estudiante,
            docente_Correspondiente_progreso=docente_curso,
            parte_cuerpo=etapa.ParteCuerpo,
            etapa_completada=etapa,
            video_visto=True,
        )
        return True
    return False


def lista_videos_curso(request, curso_id):
    """Vista para que estudiantes vean videos de un curso específico"""
    estudiante_id = request.session.get('usuario_id')
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Obtener casos clínicos del CURSO ESPECÍFICO
    casos_clinicos = Caso_clinico.objects.filter(Curso=curso)
    
    # Estructurar datos para el template
    videos_data = []
    for caso in casos_clinicos:
        partes_cuerpo = Partes_cuerpo.objects.filter(CasoClinico=caso)
        
        for parte in partes_cuerpo:
            etapas = Etapa.objects.filter(ParteCuerpo=parte)
            
            for etapa in etapas:
                # Verificar si el estudiante ya vio este video
                video_visto = Progreso.objects.filter(
                    progreso_estudiante=estudiante,
                    etapa_completada=etapa,
                    video_visto=True
                ).exists()
                
                videos_data.append({
                    'caso': caso,
                    'parte': parte,
                    'etapa': etapa,
                    'video_visto': video_visto
                })
    
    return render(request, 'estudiante/lista_videos.html', {
        'videos_data': videos_data,
        'curso_actual': curso
    })
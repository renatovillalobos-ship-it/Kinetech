

from django.shortcuts import render, get_object_or_404
from Applications.Caso_Clinico.models import (
    Caso_clinico, Partes_cuerpo, Pacientes, 
    Etapa, PreguntaEtapa, RespuestaEtapa, Partes_paciente
)
import json
from django.db.models import Prefetch

# CORREGIDO: Cambia 'casos/' por 'caso_clinico/'
def lista_casos_clinicos(request, curso_id):
    casos = Caso_clinico.objects.filter(Curso_id=curso_id).select_related('Curso')
    return render(request, 'casos/lista_casos.html', {  # ← CAMBIADO
        'casos': casos,
        'curso_id': curso_id
    })

#def detalle_caso_clinico(request, caso_id):
    #"""Paso 1: Muestra el caso clínico y sus partes del cuerpo"""
    #caso = get_object_or_404(Caso_clinico, id=caso_id)
    
    # Obtener partes del cuerpo con sus relaciones
    #partes_cuerpo = Partes_cuerpo.objects.filter(CasoClinico=caso).prefetch_related(
        #'partes_paciente_set__Pacientes',
        #'etapa_set'
    #)
    
    # Agregar icono a cada parte
    #for parte in partes_cuerpo:
        #parte.icono = obtener_icono_parte_cuerpo(parte.ParteCuerpo)
    
    #return render(request, 'casos/detalle_casos.html', {
        #'caso': caso,
        #'partes_cuerpo': partes_cuerpo,
    #})


# Applications/Caso_Clinico/views.py (función detalle_caso_clinico)

def detalle_caso_clinico(request, caso_id):
    """Paso 1: Muestra el caso clínico y sus partes del cuerpo"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    
    # Obtener partes del cuerpo con sus relaciones
    partes_cuerpo = Partes_cuerpo.objects.filter(CasoClinico=caso).prefetch_related(
        Prefetch('partes_paciente_set', queryset=Partes_paciente.objects.select_related('Pacientes')),
        'etapa_set'
    )
    
    # Agregar icono y datos de pacientes a cada parte
    for parte in partes_cuerpo:
        parte.icono = obtener_icono_parte_cuerpo(parte.ParteCuerpo)
        # Acceder a los pacientes a través de la relación intermedia para el template
        parte.pacientes = [pp.Pacientes for pp in parte.partes_paciente_set.all()]
        # Contar etapas
        parte.etapas_count = parte.etapa_set.count() # Añadimos el conteo de etapas
    
    return render(request, 'casos/detalle_casos.html', {
        'caso': caso,
        'partes_cuerpo': partes_cuerpo,
    })


def seleccionar_paciente(request, caso_id, parte_id):
    """Muestra los pacientes relacionados con una parte del cuerpo"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    parte = get_object_or_404(Partes_cuerpo, id=parte_id)
    
    # Obtener las relaciones entre parte y pacientes
    relaciones = Partes_paciente.objects.filter(
        ParteCuerpo=parte
    ).select_related('Pacientes').order_by('id')
    
    # CORRECCIÓN IMPORTANTE: Apuntar a 'casos/seleccionar_paciente.html'
    return render(request, 'casos/seleccionar_paciente.html', {
        'caso': caso,
        'parte': parte,
        'relaciones': relaciones,
    })

def ver_etapas(request, caso_id, parte_id, paciente_id):
    """Muestra las etapas de evaluación para una parte del cuerpo"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    parte = get_object_or_404(Partes_cuerpo, id=parte_id)
    paciente = get_object_or_404(Pacientes, id=paciente_id)
    
    # Obtener todas las etapas para esta parte del cuerpo
    etapas = Etapa.objects.filter(
        ParteCuerpo=parte
    ).order_by('id')
    
    # Para cada etapa, verificar si tiene video o preguntas
    for etapa in etapas:
        etapa.tiene_video = bool(etapa.video)
        etapa.tiene_preguntas = PreguntaEtapa.objects.filter(Etapa=etapa).exists()

    # APLICAR CONVERSIÓN DE URL AQUÍ:
        if etapa.tiene_video:
            etapa.video_embed = convertir_url_youtube_a_embed(etapa.video) # Creamos un nuevo atributo
    
    
    return render(request, 'casos/ver_etapas.html', {
        'caso': caso,
        'parte': parte,
        'paciente': paciente,
        'etapas': etapas,
    })

def etapa_detalle(request, caso_id, parte_id, paciente_id, etapa_id):
    """Muestra el detalle de una etapa específica"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    parte = get_object_or_404(Partes_cuerpo, id=parte_id)
    paciente = get_object_or_404(Pacientes, id=paciente_id)
    etapa = get_object_or_404(Etapa, id=etapa_id, ParteCuerpo=parte)
    
    # Verificar si la etapa tiene video
    tiene_video = bool(etapa.video)
    
    # Obtener preguntas si las tiene
    preguntas = []
    if not tiene_video:
        preguntas = PreguntaEtapa.objects.filter(Etapa=etapa).prefetch_related('respuestaetapa_set')
    
    # Obtener todas las etapas para navegación
    todas_etapas = Etapa.objects.filter(ParteCuerpo=parte).order_by('id')
    etapas_list = list(todas_etapas)
    
    try:
        index_actual = etapas_list.index(etapa)
        etapa_anterior = etapas_list[index_actual - 1] if index_actual > 0 else None
        etapa_siguiente = etapas_list[index_actual + 1] if index_actual < len(etapas_list) - 1 else None
    except ValueError:
        etapa_anterior = None
        etapa_siguiente = None
    
    return render(request, 'casos/etapa_detalle.html', {
        'caso': caso,
        'parte': parte,
        'paciente': paciente,
        'etapa': etapa,
        'tiene_video': tiene_video,
        'preguntas': preguntas,
        'etapa_anterior': etapa_anterior,
        'etapa_siguiente': etapa_siguiente,
        'total_etapas': len(etapas_list),
        'etapa_actual_numero': index_actual + 1 if 'index_actual' in locals() else 1,
    })
def obtener_icono_parte_cuerpo(nombre_parte):
    """Determina el ícono apropiado para cada parte del cuerpo"""
    nombre = nombre_parte.lower()
    
    iconos = {
        'columna': 'fas fa-bone',
        'espalda': 'fas fa-bone',
        'vertebral': 'fas fa-bone',
        'hombro': 'fas fa-hand',
        'brazo': 'fas fa-hand',
        'codo': 'fas fa-hand',
        'mano': 'fas fa-hand',
        'muñeca': 'fas fa-hand',
        'pierna': 'fas fa-running',
        'rodilla': 'fas fa-running',
        'tobillo': 'fas fa-running',
        'pie': 'fas fa-running',
        'cadera': 'fas fa-running',
        'cabeza': 'fas fa-head-side-mask',
        'cuello': 'fas fa-head-side-mask',
        'atm': 'fas fa-head-side-mask',
        'tórax': 'fas fa-lungs',
        'abdomen': 'fas fa-lungs',
        'pecho': 'fas fa-lungs',
        'general': 'fas fa-user-md',
        'corazón': 'fas fa-heartbeat',
        'pulmón': 'fas fa-lungs'
    }
    
    for clave, icono in iconos.items():
        if clave in nombre:
            return icono
    
    return 'fas fa-user-md'

# NUEVA FUNCIÓN DE AYUDA
def convertir_url_youtube_a_embed(url):
    """
    Convierte una URL normal de YouTube (watch?v=) a una URL de incrustación (embed/).
    Si la URL ya es de incrustación o no es de YouTube, la devuelve sin cambios.
    """
    if not url:
        return url
    
    # Si ya es una URL de incrustación, la devolvemos
    if 'embed/' in url:
        return url
        
    import re
    # Patrón para extraer el código del video de una URL "watch"
    patron = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)')
    
    match = patron.search(url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
        
    return url
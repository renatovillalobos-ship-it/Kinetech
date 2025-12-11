from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch
import json
import json
from Applications.Caso_Clinico.models import (
    Caso_clinico, Partes_cuerpo, Pacientes, 
    Etapa, PreguntaEtapa, RespuestaEtapa, Partes_paciente,
    TemaConsulta, OpcionTema
)
from django.views.generic import DetailView

# En views.py - Corregir VideoDetailView
class VideoDetailView(DetailView):
    model = Etapa  # Cambiar de Etapa.video a Etapa
    template_name = "video.html"
    context_object_name = "etapa"  # Cambiar de video a etapa
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['embed_url'] = self.object.embed_url() if self.object.video else None
        return context

def lista_casos_clinicos(request, curso_id):
    casos = Caso_clinico.objects.filter(Curso_id=curso_id).select_related('Curso')
    return render(request, 'casos/lista_casos.html', {
        'casos': casos,
        'curso_id': curso_id
    })


def detalle_caso_clinico(request, caso_id):
    """Paso 1: Muestra el caso clínico y sus partes del cuerpo"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    
    partes_cuerpo = Partes_cuerpo.objects.filter(CasoClinico=caso).prefetch_related(
        Prefetch('partes_paciente_set', queryset=Partes_paciente.objects.select_related('Pacientes')),
        'etapa_set'
    )
    
    for parte in partes_cuerpo:
        parte.icono = obtener_icono_parte_cuerpo(parte.ParteCuerpo)
        parte.pacientes = [pp.Pacientes for pp in parte.partes_paciente_set.all()]
        parte.etapas_count = parte.etapa_set.count()
    
    return render(request, 'casos/detalle_casos.html', {
        'caso': caso,
        'partes_cuerpo': partes_cuerpo,
    })


def seleccionar_paciente(request, caso_id, parte_id):
    """Muestra los pacientes relacionados con una parte del cuerpo"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    parte = get_object_or_404(Partes_cuerpo, id=parte_id)
    
    relaciones = Partes_paciente.objects.filter(
        ParteCuerpo=parte
    ).select_related('Pacientes').order_by('id')
    
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
    
    etapas = Etapa.objects.filter(ParteCuerpo=parte).order_by('orden')
    
    for etapa in etapas:
        etapa.tiene_video = bool(etapa.video)
        etapa.tiene_preguntas = etapa.preguntas.exists()
        if etapa.tiene_video:
            etapa.embed_url = etapa.embed_url()
    
    return render(request, 'casos/ver_etapas.html', {
        'caso': caso,
        'parte': parte,
        'paciente': paciente,
        'etapas': etapas,
    })


def etapa_detalle(request, caso_id, parte_id, paciente_id, etapa_id):
    # Obtener objetos
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    parte = get_object_or_404(Partes_cuerpo, id=parte_id)
    paciente = get_object_or_404(Pacientes, id=paciente_id)
    etapa = get_object_or_404(Etapa, id=etapa_id)
    
    embed_url = None
    if etapa.video:
        embed_url = etapa.embed_url()
    # Obtener etapas relacionadas
    todas_etapas = Etapa.objects.filter(ParteCuerpo=parte).order_by('orden')
    etapa_actual_numero = list(todas_etapas).index(etapa) + 1
    total_etapas = todas_etapas.count()
    
    # NO asignar a la propiedad, usar un atributo diferente si es necesario
    # O simplemente usar la propiedad directamente en el template
    
    try:
        etapa_anterior = todas_etapas.get(orden=etapa.orden - 1)
    except Etapa.DoesNotExist:
        etapa_anterior = None
        
    try:
        etapa_siguiente = todas_etapas.get(orden=etapa.orden + 1)
    except Etapa.DoesNotExist:
        etapa_siguiente = None
    
    # Contexto base
    contexto = {
        'caso': caso,
        'parte': parte,
        'paciente': paciente,
        'etapa': etapa,
        'embed_url': embed_url, 
        'etapa_actual_numero': etapa_actual_numero,
        'total_etapas': total_etapas,
        'etapa_anterior': etapa_anterior,
        'etapa_siguiente': etapa_siguiente,
    }
    
    # Datos específicos por tipo de etapa
    if etapa.tipo == 'formulario_temas':
        # Obtener temas para esta etapa
        temas = TemaConsulta.objects.filter(etapa=etapa).order_by('orden')
        contexto['temas'] = temas
    
    elif etapa.tipo == 'preguntas_tema':
        # Obtener preguntas para esta etapa
        preguntas = PreguntaEtapa.objects.filter(Etapa=etapa).prefetch_related('respuestas')
        contexto['preguntas'] = preguntas
    else:
        DetailView()
    
    return render(request, 'casos/etapa_detalle.html', contexto)





@csrf_exempt
def api_opciones_tema(request, tema_id):
    """API para obtener opciones de un tema específico"""
    try:
        tema = get_object_or_404(TemaConsulta, id=tema_id)
        opciones = OpcionTema.objects.filter(tema=tema).order_by('id')
        
        opciones_data = [
            {
                'id': opcion.id,
                'texto': opcion.texto,
                'es_correcta': opcion.es_correcta,
                'retroalimentacion': opcion.retroalimentacion or '',
                'lleva_a_etapa': opcion.lleva_a_etapa.id if opcion.lleva_a_etapa else None
            }
            for opcion in opciones
        ]
        
        return JsonResponse({
            "success": True,
            "tema_id": tema_id,
            "tema_nombre": tema.nombre,
            "opciones": opciones_data
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": str(e)
        }, status=500)

@csrf_exempt
def procesar_respuesta(request, caso_id, parte_id, paciente_id, etapa_id):
    """Procesar respuesta del usuario en etapa de formulario de temas"""
    if request.method == 'POST':
        try:
            opcion_id = request.POST.get('opcion_id')
            
            # Obtener la opción seleccionada
            opcion = get_object_or_404(OpcionTema, id=opcion_id)
            
            # Obtener contexto
            caso = get_object_or_404(Caso_clinico, id=caso_id)
            parte = get_object_or_404(Partes_cuerpo, id=parte_id)
            paciente = get_object_or_404(Pacientes, id=paciente_id)
            etapa = get_object_or_404(Etapa, id=etapa_id, ParteCuerpo=parte)
            
            # Guardar la respuesta en sesión
            if 'respuestas_caso' not in request.session:
                request.session['respuestas_caso'] = {}
            
            key = f"{caso_id}_{parte_id}_{paciente_id}_{etapa_id}"
            request.session['respuestas_caso'][key] = {
                'opcion_id': opcion_id,
                'correcta': opcion.es_correcta,
                'retroalimentacion': opcion.retroalimentacion,
                'fecha': str(datetime.now())
            }
            request.session.modified = True
            
            # Determinar qué hacer según si es correcta o no
            if opcion.es_correcta:
                # Si tiene redirección específica
                if opcion.lleva_a_etapa:
                    siguiente_etapa = opcion.lleva_a_etapa
                else:
                    # Buscar siguiente etapa del mismo tipo o la siguiente en orden
                    siguiente_etapa = Etapa.objects.filter(
                        ParteCuerpo=parte,
                        orden__gt=etapa.orden
                    ).order_by('orden').first()
                
                if siguiente_etapa:
                    return JsonResponse({
                        'success': True,
                        'correcta': True,
                        'redirect': True,
                        'url': reverse('Caso_Clinico:etapa_detalle', 
                                     args=[caso_id, parte_id, paciente_id, siguiente_etapa.id])
                    })
                else:
                    # No hay más etapas
                    return JsonResponse({
                        'success': True,
                        'correcta': True,
                        'redirect': True,
                        'url': reverse('Caso_Clinico:ver_progreso', 
                                     args=[caso_id, parte_id, paciente_id])
                    })
            else:
                # Respuesta incorrecta - quedarse en la misma etapa
                return JsonResponse({
                    'success': True,
                    'correcta': False,
                    'redirect': False,
                    'retroalimentacion': opcion.retroalimentacion or "Respuesta incorrecta. Intente nuevamente."
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


def ver_progreso(request, caso_id, parte_id, paciente_id):
    """Muestra el progreso del caso"""
    caso = get_object_or_404(Caso_clinico, id=caso_id)
    parte = get_object_or_404(Partes_cuerpo, id=parte_id)
    paciente = get_object_or_404(Pacientes, id=paciente_id)
    
    etapas = Etapa.objects.filter(ParteCuerpo=parte).order_by('orden')
    
    # Obtener respuestas de sesión
    respuestas = request.session.get('respuestas_caso', {})
    etapas_completadas = 0
    
    for etapa in etapas:
        key = f"{caso_id}_{parte_id}_{paciente_id}_{etapa.id}"
        if key in respuestas:
            etapas_completadas += 1
    
    progreso_porcentaje = (etapas_completadas / len(etapas)) * 100 if etapas else 0
    
    return render(request, 'casos/progreso.html', {
        'caso': caso,
        'parte': parte,
        'paciente': paciente,
        'etapas': etapas,
        'respuestas': respuestas,
        'progreso_porcentaje': progreso_porcentaje,
        'etapas_completadas': etapas_completadas,
        'total_etapas': len(etapas),
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
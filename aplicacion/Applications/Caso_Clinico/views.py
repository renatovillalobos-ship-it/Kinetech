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
    Etapa, Partes_paciente,
    TemaConsulta, OpcionTema, Diagnostico_Tratamiento
)
from django.views.generic import DetailView

class VideoDetailView(DetailView):
    model = Etapa  
    template_name = "video.html"
    context_object_name = "etapa"  
    
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
    todas_etapas = Etapa.objects.filter(ParteCuerpo=parte).order_by('orden')
    etapa_actual_numero = list(todas_etapas).index(etapa) + 1
    total_etapas = todas_etapas.count()
    
    try:
        etapa_anterior = todas_etapas.get(orden=etapa.orden - 1)
    except Etapa.DoesNotExist:
        etapa_anterior = None
        
    try:
        etapa_siguiente = todas_etapas.get(orden=etapa.orden + 1)
    except Etapa.DoesNotExist:
        etapa_siguiente = None

    if etapa_siguiente:
        next_url = reverse('Caso_Clinico:etapa_detalle', kwargs={
            'caso_id': caso_id,
            'parte_id': parte_id,
            'paciente_id': paciente_id,
            'etapa_id': etapa_siguiente.id
        })
    else:
        next_url = reverse('Caso_Clinico:detalle_caso', kwargs={
            'caso_id': caso_id
        })
    
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
        'next_url': next_url,
    }
    if etapa.tipo == 'formulario_temas':
        temas = TemaConsulta.objects.filter(etapa=etapa).order_by('orden')
        contexto['temas'] = temas
        
    elif etapa.tipo in ['diagnosticos', 'tratamientos']:
        contenidos = etapa.contenidos.all().order_by('orden')
        
        contexto['diagnosticos'] = contenidos.filter(tipo='diagnostico')
        contexto['tratamientos'] = contenidos.filter(tipo='tratamiento')
        
    else:
        pass 
    
    return render(request, 'casos/etapa_detalle.html', contexto)

@csrf_exempt
def api_opciones_tema(request, tema_id):
    try:
        tema = get_object_or_404(TemaConsulta, id=tema_id)
        opciones = OpcionTema.objects.filter(tema=tema).order_by('id')
        
        opciones_data = []
        for opcion in opciones:
            opcion_data = {
                'id': opcion.id,
                'texto': opcion.texto,
                'es_correcta': opcion.es_correcta,
                'retroalimentacion': opcion.retroalimentacion or '',
                'video_respuesta': opcion.video_respuesta or '',
                'embed_url_video': opcion.embed_url(),  # IMPORTANTE: usar el método embed_url()
            }
            opciones_data.append(opcion_data)
        
        return JsonResponse({
            "success": True,
            "tema_id": tema_id,
            "tema_nombre": tema.nombre,
            "opciones": opciones_data
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
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


@csrf_exempt
def api_diagnosticos(request, etapa_id):
    """Retorna los diagnósticos y tratamientos de una Etapa en formato JSON."""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        contenidos = Diagnostico_Tratamiento.objects.filter(etapa_id=etapa_id).order_by('orden', 'id')
        
        data_diagnosticos = []
        for contenido in contenidos:
            data_diagnosticos.append({
                'id': contenido.id,
                'titulo': contenido.titulo,
                'descripcion': contenido.descripcion,
                'tipo': contenido.tipo,
            })
            
        return JsonResponse({
            'success': True,
            'etapa_id': etapa_id,
            'diagnosticos': data_diagnosticos
        })
        
    except Exception as e:
        print(f"Error al obtener diagnósticos de la etapa {etapa_id}: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

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
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Count
from Applications.Cuestionario.models import cuestionario
from Applications.Estudiante.models import ResultadoCuestionario

import os

from ..Docente.models import Curso
from .models import Estudiante, Progreso
from Applications.Caso_Clinico.models import Caso_clinico, Etapa 


# ------------------
import time
from django.http import JsonResponse

# ✅ AGREGAR ESTE IMPORT
from django.contrib.auth import get_user_model
import re  # ← ESTO FALTA EN EL ARCHIVO
# ------------------

# -----------------------------------------------------------
# HOME ESTUDIANTE (PROTEGIDO POR SESIÓN)
# -----------------------------------------------------------
class Home_estudiante(TemplateView):
    template_name = 'estudiante/home_estudiante.html'

    def get(self, request, *args, **kwargs):
        # Bloquea acceso si no está logueado
        if request.session.get('usuario_tipo') != 'estudiante':
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        estudiante_id = self.request.session.get('usuario_id')
        if estudiante_id:
            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                context['estudiante'] = estudiante

                # Obtener cursos asignados
                cursos_asignados = estudiante.cursos.all()
                context['cursos'] = cursos_asignados  # ← CAMBIÉ 'cursos_asignados' a 'cursos'
                
                # Cursos NO asignados al estudiante
                cursos_disponibles = Curso.objects.exclude(id__in=cursos_asignados)
                context['cursos_disponibles'] = cursos_disponibles

                if cursos_asignados.exists():
                    # Contar videos de todos los cursos asignados
                    total_videos = Etapa.objects.filter(
                        ParteCuerpo__CasoClinico__Curso__in=cursos_asignados
                    ).count()

                    context['tiene_videos'] = total_videos > 0
                    context['total_videos'] = total_videos
                else:
                    context['tiene_videos'] = False
                    context['total_videos'] = 0

            except Estudiante.DoesNotExist:
                context['tiene_videos'] = False
                context['total_videos'] = 0
                context['cursos'] = []

        return context


class CerrarSesion(View):
    def get(self, request):
        request.session.flush() 
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect('login')

# -----------------------------------------------------------
# PROGRESO
# -----------------------------------------------------------

def calcular_progreso_estudiante(estudiante):
    cursos = estudiante.cursos.all()

    if not cursos.exists():
        return 0  # SIN CURSOS = 0%

    # --- VIDEOS TOTALES ---
    total_videos = Etapa.objects.filter(
        ParteCuerpo__CasoClinico__Curso__in=cursos
    ).count()

    # --- VIDEOS VISTOS ---
    videos_vistos = Progreso.objects.filter(
        progreso_estudiante=estudiante,
        video_visto=True
    ).values('etapa_completada').distinct().count()

    # --- CUESTIONARIOS TOTALES ---
    cuestionarios_totales = cuestionario.objects.filter(
        Curso__in=cursos
    ).count()

    # --- CUESTIONARIOS COMPLETADOS ---
    cuestionarios_completados = ResultadoCuestionario.objects.filter(
        estudiante=estudiante
    ).values('cuestionario').distinct().count()

    # --- ACTIVIDADES TOTALES ---
    total_actividades = total_videos + cuestionarios_totales
    actividades_completadas = videos_vistos + cuestionarios_completados

    if total_actividades == 0:
        return 0

    progreso_final = (actividades_completadas / total_actividades) * 100
    return round(progreso_final, 2)

# -----------------------------------------------------------
# PERFIL ESTUDIANTE
# -----------------------------------------------------------
class Perfil_estudiante(TemplateView):
    template_name = 'estudiante/perfil_estudiante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        estudiante_id = self.request.session.get('usuario_id')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        context['estudiante'] = estudiante

        progreso_obj = Progreso.objects.filter(progreso_estudiante=estudiante).first()
        context['progreso'] = calcular_progreso_estudiante(estudiante)


        return context


# -----------------------------------------------------------
# SUBIR FOTO
# -----------------------------------------------------------
def subir_foto_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')

        if not foto:
            messages.error(request, "Debes seleccionar una imagen.")
            return redirect('estudiante:perfil_estudiante')

        # Intentar validar imagen antes de guardar
        try:
            estudiante.foto_perfil_estudiante.field.clean(foto, estudiante)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('estudiante:perfil_estudiante')

        # Eliminar foto anterior (si existía)
        if estudiante.foto_perfil_estudiante:
            try:
                if os.path.isfile(estudiante.foto_perfil_estudiante.path):
                    os.remove(estudiante.foto_perfil_estudiante.path)
            except:
                pass

        # Guardar nueva imagen
        estudiante.foto_perfil_estudiante = foto
        estudiante.save()

        messages.success(request, "Foto actualizada correctamente.")
        return redirect('estudiante:perfil_estudiante')

    return redirect('estudiante:perfil_estudiante')


# -----------------------------------------------------------
# ELIMINAR FOTO
# -----------------------------------------------------------
def eliminar_foto_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)

    if estudiante.foto_perfil_estudiante:
        if os.path.isfile(estudiante.foto_perfil_estudiante.path):
            os.remove(estudiante.foto_perfil_estudiante.path)

        estudiante.foto_perfil_estudiante = None
        estudiante.save()
        messages.success(request, "Foto eliminada correctamente.")

    return redirect('estudiante:perfil_estudiante')


# -----------------------------------------------------------
# REGISTRO ESTUDIANTE
# -----------------------------------------------------------
class RegistroEstudiante(View):
    template_name = 'login/login.html'
    success_url_name = 'login'

    def post(self, request):
        inicio = time.time()  # ✅ INICIAR MEDICIÓN

        nombre = request.POST.get('nombre_est')
        apellido = request.POST.get('apellido_est')
        pais = request.POST.get('pais_est')
        correo = request.POST.get('correo_est')
        password = request.POST.get('password_est')

        # Validaciones
        if not all([nombre, apellido, pais, correo, password]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, self.template_name)

        if not correo.endswith('@alumnos.ucn.cl'):
            messages.error(request, "El correo debe terminar en @alumnos.ucn.cl.")
            return render(request, self.template_name)
        
         # VERIFICAR SI EL CORREO YA EXISTE
        if Estudiante.objects.filter(correo_estudiante=correo).exists():
            messages.error(request, f"El correo {correo} ya está registrado.")
            return render(request, self.template_name)

        try:
            hashed_password = make_password(password)

           # CREAR ESTUDIANTE SIN curso_estudiante_id fijo
            Estudiante.objects.create(
                nombre_estudiante=nombre,
                apellido_estudiante=apellido,
                pais_estudiante=pais,
                correo_estudiante=correo,
                contrasena_estudiante=hashed_password,
                #curso_estudiante_id=2,
                foto_perfil_estudiante=None
            )

            # cambios
            tiempo = round(time.time() - inicio, 2)  # ✅ CALCULAR TIEMPO
    
            messages.success(request, f"¡Registro exitoso en {tiempo} segundos! Ahora puedes iniciar sesión.")
          
            messages.error(request, "Correo ya registrado", extra_tags="estudiante")


            #messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect(self.success_url_name)
        
        except Exception as e:
             # cambios
            tiempo = round(time.time() - inicio, 2)
            messages.error(request, f"Error en el registro ({tiempo}s): {str(e)}")
    
            #messages.error(request, f"Error en el registro: {str(e)}")
            return render(request, self.template_name)

       # except IntegrityError:
        #    messages.error(request, "Este correo ya está registrado.")
        #    return render(request, self.template_name)


# -----------------------------------------------------------
# LOGIN
# -----------------------------------------------------------
def login_estudiante(request):
    return render(request, 'estudiante/login.html')


# -----------------------------------------------------------
# AUTENTICAR
# -----------------------------------------------------------
def autenticar_estudiante(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        remember_me = request.POST.get('remember_me')  # 'on' si está marcado

        # ✅ BLOQUEO 3 INTENTOS (AGREGAR)
        intentos = request.session.get(f'bloqueo_{correo}', 0)
        if intentos >= 3:
            print(f"📧 Email bloqueo a: {correo}")
            return render(request, 'Login/blocked.html')
        # ✅ FIN BLOQUEO


        estudiante = Estudiante.objects.filter(correo_estudiante=correo).first()

        if not estudiante or not check_password(contrasena, estudiante.contrasena_estudiante):
     # ---------------
            # ❌ FALLÓ: Contar intento
            intentos += 1
            request.session[f'bloqueo_{correo}'] = intentos
            
            if intentos >= 3:
                print(f"📧 Email bloqueo a: {correo}")
                messages.error(request, "Bloqueado por 3 intentos. Usa 'Restablecer contraseña'.")
                return render(request, 'Login/blocked.html')
            
            messages.error(request, f"Error. Intentos: {intentos}/3")
     # ---------------------------
            
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('estudiante:login')
        
        # ---------------
        # ✅ ÉXITO: Resetear bloqueo
        request.session.pop(f'bloqueo_{correo}', None)
        # LIMPIAR sesión anterior
        request.session.flush()
        # ---------------

        # Crear sesión
        request.session['usuario_tipo'] = 'estudiante'
        request.session['usuario_id'] = estudiante.id

        # --------
        # IMPLEMENTAR "RECORDARME" - FUNCIONALIDAD REQUERIDA AL 100%
        if remember_me:
            # Sesión de 30 días (2592000 segundos)
            request.session.set_expiry(2592000)
            print("✓ Estudiante - Recordarme ACTIVADO (30 días)")
        else:
            # Sesión de navegador (se cierra al cerrar el navegador)
            request.session.set_expiry(0)
            print("✓ Estudiante - Recordarme DESACTIVADO (sesión navegador)")
         # ------

        return redirect('estudiante:home_estudiante')

    return redirect('estudiante:login')


def validar_correo_ucn(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    inicio = time.time()

    correo = request.POST.get('correo', '').strip().lower()

    # Validación robusta del correo institucional
    patron = r'^[a-zA-Z0-9\.\-_]+@alumnos\.ucn\.cl$'
    es_valido = bool(re.match(patron, correo))

    tiempo = round(time.time() - inicio, 4)

    if es_valido:
        return JsonResponse({
            'valido': True,
            'mensaje': 'Correo institucional válido',
            'tiempo': tiempo
        })

    return JsonResponse({
        'valido': False,
        'mensaje': 'Solo se permiten correos @alumnos.ucn.cl',
        'tiempo': tiempo
    })


# -----------------------------------------------------------
# VALIDACIÓN RÁPIDA DE EXISTENCIA DE CUENTA
# -----------------------------------------------------------
def validar_existencia_cuenta(request):
    """Valida si una cuenta existe en menos de 10 segundos"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    inicio = time.time()
    correo = request.POST.get('correo', '').strip().lower()
    
    # Validación ultra-rápida
    existe_estudiante = Estudiante.objects.filter(correo_estudiante=correo).exists()
    
    # También verificar docente
    User = get_user_model()
    existe_docente = User.objects.filter(email=correo).exists()
    
    cuenta_existe = existe_estudiante or existe_docente
    
    tiempo = round(time.time() - inicio, 4)

    return JsonResponse({
        'existe': cuenta_existe,
        'mensaje': '✓ Cuenta encontrada' if cuenta_existe else '✗ Cuenta no registrada',
        'tiempo': tiempo,
        'tipo': 'estudiante' if existe_estudiante else 'docente' if existe_docente else 'none'
    })


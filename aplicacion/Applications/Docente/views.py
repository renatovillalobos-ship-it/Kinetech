from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.db import transaction
import os
import re  
import time
from django.http import JsonResponse
from django.db.models import Count, Prefetch
from ..Estudiante.models import Estudiante, Progreso  
from .models import Docente, Curso
from Applications.Caso_Clinico.models import Caso_clinico, Partes_cuerpo, Etapa
from django.shortcuts import redirect

class LoginRequeridoDocenteMixin(View):
    login_url = '/docente/login/'

    def dispatch(self, request, *args, **kwargs):

        usuario_tipo = request.session.get('usuario_tipo')
        usuario_id = request.session.get('usuario_id')
        
        if usuario_tipo != 'docente' or not usuario_id:
            return redirect(self.login_url)
        
        try:
            docente = Docente.objects.get(id=usuario_id)
        except Docente.DoesNotExist:
            request.session.flush()
            return redirect(self.login_url)
            
        return super().dispatch(request, *args, **kwargs)


# LOGIN DOCENTE
class Login(TemplateView):
    template_name = 'login/login.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        asignaturas = (
            Curso.objects.values_list('nombre_del_Curso', flat=True)
            .distinct()
            .order_by('nombre_del_Curso')
        )

        context['asignaturas'] = asignaturas
        return context


    def get(self, request, *args, **kwargs):

        usuario_tipo = request.session.get('usuario_tipo')
        usuario_id = request.session.get('usuario_id')
        
        if usuario_tipo and usuario_id and request.session.get_expiry_age() > 0:

            try:
                if usuario_tipo == 'docente':
                    Docente.objects.get(id=usuario_id)
                    return redirect('docente:home_docente')

                elif usuario_tipo == 'estudiante':
                    Estudiante.objects.get(id=usuario_id)
                    return redirect('estudiante:home_estudiante')

            except (Docente.DoesNotExist, Estudiante.DoesNotExist):
                request.session.flush()

        return super().get(request, *args, **kwargs)


# HOME DOCENTE (PROTEGIDO POR SESIÓN)
class Home_docente(TemplateView):
    template_name = 'docente/home_docente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        docente_id = self.request.session.get('usuario_id')
        docente = get_object_or_404(Docente, id=docente_id)

        context['docente'] = docente
    
        if docente.curso_principal:
            context['cursos'] = [docente.curso_principal]
        else:
            context['cursos'] = Curso.objects.none()

        return context


# VISTA PARA DETALLE Y PROGRESO
def detalle_curso(request, id):
    curso = get_object_or_404(Curso, id=id) 
    contexto = {'curso': curso}
    return render(request, 'docente/detalle_curso.html', contexto)


class ProgresoDocenteView(LoginRequeridoDocenteMixin, TemplateView):
    template_name = 'docente/progreso_docente.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('curso_id')
        
        docente_id = self.request.session.get('usuario_id')
        if docente_id:
            try:
                docente = Docente.objects.get(id=docente_id)
                context['cursos'] = Curso.objects.filter(docentes=docente)
                
                if curso_id:
                    curso_seleccionado = get_object_or_404(
                    Curso, 
                    id=curso_id, 
                    docentes=docente
                    )
                
                    context['curso_seleccionado'] = curso_seleccionado
                    
                    estudiantes_curso = Estudiante.objects.filter(
                        cursos=curso_seleccionado
                    ).select_related().order_by('apellido_estudiante', 'nombre_estudiante')
                    
                    casos_clinicos = Caso_clinico.objects.filter(
                        Curso=curso_seleccionado
                    ).prefetch_related('partes_cuerpo_set__etapa_set')
                    
                    progresos_curso = Progreso.objects.filter(
                        progreso_curso=curso_seleccionado,
                        video_visto=True
                    ).values('progreso_estudiante', 'parte_cuerpo').annotate(
                        total_videos_vistos=Count('id')
                    )
                    
                    progresos_dict = {}
                    for p in progresos_curso:
                        key = (p['progreso_estudiante'], p['parte_cuerpo'])
                        progresos_dict[key] = p['total_videos_vistos']
                    
                    progreso_data = []
                    
                    for estudiante in estudiantes_curso:
                        total_videos_curso = 0
                        total_vistos_estudiante = 0
                        progreso_casos = []
                        
                        for caso in casos_clinicos:
                            progreso_caso = {
                                'caso': caso,
                                'partes_cuerpo': []
                            }
                            
                            for parte in caso.partes_cuerpo_set.all():
                                total_videos_parte = parte.etapa_set.count()
                                total_videos_curso += total_videos_parte
                                
                                if total_videos_parte > 0:
                                    videos_vistos = progresos_dict.get(
                                        (estudiante.id, parte.id), 
                                        0
                                    )
                                    total_vistos_estudiante += videos_vistos
                                    porcentaje = (videos_vistos / total_videos_parte) * 100
                                    
                                    if porcentaje == 0:
                                        color = 'danger'
                                    elif porcentaje < 70:
                                        color = 'warning'
                                    else:
                                        color = 'success'
                                    
                                    progreso_caso['partes_cuerpo'].append({
                                        'parte': parte,
                                        'total_videos': total_videos_parte,
                                        'videos_vistos': videos_vistos,
                                        'porcentaje': round(porcentaje, 1),
                                        'color': color
                                    })
                            
                            if progreso_caso['partes_cuerpo']:
                                progreso_casos.append(progreso_caso)
                        
                        if total_videos_curso > 0:
                            progreso_promedio = (total_vistos_estudiante / total_videos_curso) * 100
                        else:
                            progreso_promedio = 0
                        
                        if progreso_promedio == 0:
                            color_general = 'danger'
                        elif progreso_promedio < 70:
                            color_general = 'warning'
                        else:
                            color_general = 'success'
                        
                        progreso_data.append({
                            'estudiante': estudiante,
                            'progreso_promedio': round(progreso_promedio, 1),
                            'color_general': color_general,
                            'total_videos_curso': total_videos_curso,
                            'total_vistos_estudiante': total_vistos_estudiante,
                            'progreso_casos': progreso_casos
                        })
                    
                    context['progreso_estudiantes'] = progreso_data
                    context['casos_clinicos'] = casos_clinicos
                    
            except Docente.DoesNotExist:
                pass
        
        return context


# PERFIL DOCENTE
class PerfilDocente(TemplateView):
    template_name = 'docente/perfil_docente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_id = self.request.session.get('usuario_id')
        docente = get_object_or_404(Docente, id=docente_id)
        context['docente'] = docente
        context['cursos'] = Curso.objects.filter(docentes=docente)
        return context


# SUBIR FOTO DOCENTE
def subir_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')
        if foto:
            docente.foto_perfil_docente = foto
            try:
                docente.foto_perfil_docente.field.clean(foto, docente)
                docente.save()
                messages.success(request, 'Foto actualizada correctamente.')
            except ValidationError as e:
                messages.error(request, e.messages[0])

    return redirect('docente:perfil_docente')


# ELIMINAR FOTO DOCENTE
def eliminar_foto_docente(request, id):
    docente = get_object_or_404(Docente, id=id)

    if docente.foto_perfil_docente:
        if os.path.isfile(docente.foto_perfil_docente.path):
            os.remove(docente.foto_perfil_docente.path)
        docente.foto_perfil_docente = None
        docente.save()
        messages.success(request, 'Foto eliminada correctamente.')

    return redirect('docente:perfil_docente')


# REGISTRO DOCENTE
from Applications.Docente.models import Curso, Docente
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.db import IntegrityError
import time
from django.utils import timezone

class RegistroDocente(View):
    template_name = 'login/login.html'
    success_url_name = 'login'

    def get(self, request):
        cursos_disponibles = Curso.objects.all()
        
        asignaturas = ['Anatomía', 'Fisiología', 'Patología', 'Farmacología', 'Otra']
        
        context = {
            'cursos_disponibles': cursos_disponibles,
            'asignaturas': asignaturas,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        inicio = time.time()

        nombre = request.POST.get('nombre_doc')
        apellido = request.POST.get('apellido_doc')
        
        curso_id = request.POST.get('curso_id')
        
        curso_seleccionado = request.POST.get('asigna_doc')
        
        pais = request.POST.get('pais_doc')
        correo = request.POST.get('correo_doc')
        password = request.POST.get('password_doc')

        if not all([nombre, apellido, correo, password]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, self.template_name)

        dominios_permitidos = ('@gmail.com', '@hotmail.com', '@ucn.cl', '@ce.ucn.cl')
        if not any(correo.endswith(d) for d in dominios_permitidos):
            messages.error(request, f"El correo debe pertenecer a uno de estos dominios: {dominios_permitidos}")
            return render(request, self.template_name)
        
        try:
            with transaction.atomic():
                # 1. Crear User de Django
                user_django = User.objects.create_user(
                    username=correo,
                    email=correo,
                    password=password,
                    first_name=nombre,
                    last_name=apellido,
                    is_staff=True
                )

                # 2. Obtener el Curso basado en la selección
                curso = None
                
                if curso_id and curso_id.isdigit():
                    try:
                        curso = Curso.objects.get(id=int(curso_id))
                    except Curso.DoesNotExist:
                        messages.error(request, "El curso seleccionado no existe.")
                        return render(request, self.template_name)
                
                elif curso_seleccionado:
                    curso, creado = Curso.objects.get_or_create(
                        nombre_del_Curso=curso_seleccionado,
                        defaults={
                            'Descripcion_del_curso': f'Curso de {curso_seleccionado}',
                            'Descripcion_breve_del_curso': curso_seleccionado,
                            'fecha_realización_curso': timezone.now().date(),
                            'paralelo_curso': 1
                        }
                    )
                else:
                    messages.error(request, "Debe seleccionar un curso/asignatura.")
                    return render(request, self.template_name)

                # 3. Crear Docente
                docente = Docente.objects.create(
                    user=user_django,
                    nombre_docente=nombre,
                    apellido_docente=apellido,
                    pais_docente=pais,
                    curso_principal=curso
                )
                
                # 4. Asignar al grupo de Docentes
                try:
                    docente_group = Group.objects.get(name='Docentes')
                    user_django.groups.add(docente_group) 
                except Group.DoesNotExist:
                    print("ADVERTENCIA: El grupo 'Docentes' no existe.")

                tiempo = round(time.time() - inicio, 2)
                messages.success(request, f"Docente {nombre} {apellido} creado en {tiempo} segundos", extra_tags="docente")
                messages.success(request, f"Asignado al curso: {curso.nombre_del_Curso}")
                
                return redirect(self.success_url_name)

        except IntegrityError:
            tiempo = round(time.time() - inicio, 2)
            messages.error(request, f"Este correo ya está registrado ({tiempo}s)")
            return render(request, self.template_name)
        except Exception as e:
            tiempo = round(time.time() - inicio, 2)
            messages.error(request, f"Error al crear docente: {str(e)} ({tiempo}s)")
            return render(request, self.template_name)


# AUTENTICAR USUARIO (ESTUDIANTE O DOCENTE)
class AutenticarUsuario(View):
    template_name = 'login/login.html'

    def post(self, request):
        correo = request.POST.get('correo')
        password = request.POST.get('contrasena')
        remember_me = request.POST.get('remember_me') 
        
        intentos_key = f'intentos_{correo}'
        intentos = request.session.get(intentos_key, 0)
        
        if intentos >= 3:
            print(f"📧 Email bloqueo enviado a: {correo}")
            return render(request, 'Login/blocked.html')

        # Verificar estudiante
        estudiante = Estudiante.objects.filter(correo_estudiante=correo).first()
        if estudiante and check_password(password, estudiante.contrasena_estudiante):
            if intentos_key in request.session:
                del request.session[intentos_key]

            request.session['usuario_tipo'] = 'estudiante'
            request.session['usuario_id'] = estudiante.id

            if remember_me:
                request.session.set_expiry(2592000)
            else:
                request.session.set_expiry(0)

            return redirect('estudiante:home_estudiante')

        # Verificar docente
        user_django = authenticate(request, username=correo, password=password)
        if user_django is not None:
            try:
                docente = Docente.objects.get(user=user_django)
                if intentos_key in request.session:
                    del request.session[intentos_key]
                
                request.session.flush()
                login(request, user_django) 

                if remember_me:
                    request.session.set_expiry(2592000)
                else:
                    request.session.set_expiry(0)
                
                request.session['usuario_tipo'] = 'docente'
                request.session['usuario_id'] = docente.pk 
                
                return redirect('docente:home_docente')
            except Docente.DoesNotExist:
                messages.error(request, "Error en el perfil de docente.")
                
        intentos += 1
        request.session[intentos_key] = intentos
        
        if intentos >= 3:
            print(f"📧 Email bloqueo enviado a: {correo}")
            messages.error(request, "Cuenta bloqueada por 3 intentos. Usa 'Restablecer contraseña'.")
            return render(request, 'Login/blocked.html')
        
        messages.error(request, "Correo o contraseña incorrectos.")
        return render(request, self.template_name)


# CERRAR SESIÓN
class CerrarSesion(View):
    def get(self, request):
        request.session.flush()
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect('login')


# PÁGINA PRINCIPAL DE CURSOS
def pagina_principal_docente(request, curso_id):

    curso = get_object_or_404(Curso, pk=curso_id)

    contexto = {
        'curso_actual': curso 
    }

    return render(request, 'docente/docente_pagina_principal.html', contexto)


# VALIDACIÓN DE CORREO UCN (FUNCIONAL Y OPTIMIZADA)
def validar_correo_ucn(request):
    """Valida correos @alumnos.ucn.cl en menos de 10 segundos"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    inicio = time.time()
    correo = request.POST.get('correo', '').strip().lower()
    
    patron = r'^[a-zA-Z0-9\.\-_]+@alumnos\.ucn\.cl$'
    es_valido = bool(re.match(patron, correo))
    
    tiempo = round(time.time() - inicio, 4)

    if es_valido:
        return JsonResponse({
            'valido': True,
            'mensaje': '✓ Correo institucional válido',
            'tiempo': tiempo
        })

    return JsonResponse({
        'valido': False,
        'mensaje': '✗ Solo se permiten correos @alumnos.ucn.cl',
        'tiempo': tiempo
    })


# VALIDACIÓN DE EXISTENCIA DE CUENTA
def validar_existencia_cuenta(request):
    """Valida si una cuenta existe en menos de 10 segundos"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    inicio = time.time()
    correo = request.POST.get('correo', '').strip().lower()
    
    User = get_user_model()
    existe_estudiante = Estudiante.objects.filter(correo_estudiante=correo).exists()
    existe_docente = User.objects.filter(email=correo).exists()
    
    cuenta_existe = existe_estudiante or existe_docente
    tiempo = round(time.time() - inicio, 4)

    return JsonResponse({
        'existe': cuenta_existe,
        'mensaje': '✓ Cuenta encontrada' if cuenta_existe else '✗ Cuenta no registrada',
        'tiempo': tiempo,
        'tipo': 'estudiante' if existe_estudiante else 'docente' if existe_docente else 'none'
    })
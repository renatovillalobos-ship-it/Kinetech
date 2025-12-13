from django.urls import path
from . import views
from . import views_videos
from . import views_ajax
from .views_ajax import (
    curso_panel, ajax_instrucciones, ajax_cuestionario, 
    ajax_caso_clinico, ajax_evaluaciones, ajax_guardar_respuestas,
    ajax_sidebar_curso 
)

app_name = 'estudiante'

urlpatterns = [
    path('login/', views.login_estudiante, name='login'),
    path('autenticar/', views.autenticar_estudiante, name='autenticar'),
    path('home_estudiante/',views.Home_estudiante.as_view(),name='home_estudiante'),
    path('registro_estudiante/', views.RegistroEstudiante.as_view(), name='registro_estudiante'),
    path('perfil_estudiante/', views.Perfil_estudiante.as_view(), name='perfil_estudiante'),
    path('subir_foto/<int:id>/', views.subir_foto_estudiante, name='subir_foto_estudiante'),
    path('eliminar_foto/<int:id>/', views.eliminar_foto_estudiante, name='eliminar_foto_estudiante'),
    path('logout/', views.CerrarSesion.as_view(), name='logout'),
    path('videos/', views_videos.lista_videos_estudiante, name='lista_videos'),
    path('ver-video/<int:etapa_id>/', views_videos.ver_video, name='ver_video'),
    path('cursos/<int:curso_id>/', views_videos.lista_videos_curso, name='curso'),
    path('curso/<int:curso_id>/', views_ajax.curso_panel, name='curso'),
    path('curso/<int:curso_id>/ajax/instrucciones/',views_ajax.ajax_instrucciones,name='ajax_instrucciones'),
    path('curso/<int:curso_id>/ajax/cuestionario/<int:cuest_id>/',views_ajax.ajax_cuestionario,name='ajax_cuestionario'),
    path('curso/<int:curso_id>/ajax/caso/',views_ajax.ajax_caso_clinico,name='ajax_caso_clinico'),
    path('curso/<int:curso_id>/ajax/evaluaciones/',views_ajax.ajax_evaluaciones,name='ajax_evaluaciones'),
    path('curso/<int:curso_id>/ajax/cuestionario/<int:cuest_id>/guardar/',views_ajax.ajax_guardar_respuestas,name='ajax_guardar_respuestas'),
    path('validar-correo-ucn/', views.validar_correo_ucn, name='validar_correo_ucn'),
    path('validar-existencia-cuenta/', views.validar_existencia_cuenta, name='validar_existencia_cuenta'),
    
    # Panel del curso y AJAX
    path('curso/<int:curso_id>/', curso_panel, name='curso_panel'),
    path('ajax/sidebar/<int:curso_id>/', ajax_sidebar_curso, name='ajax_sidebar'),  
    
    # AJAX endpoints
    path('ajax/instrucciones/<int:curso_id>/', ajax_instrucciones, name='ajax_instrucciones'),
    path('ajax/cuestionario/<int:curso_id>/<int:cuest_id>/', ajax_cuestionario, name='ajax_cuestionario'),
    path('ajax/caso-clinico/<int:curso_id>/', ajax_caso_clinico, name='ajax_caso_clinico'),
    path('ajax/evaluaciones/<int:curso_id>/', ajax_evaluaciones, name='ajax_evaluaciones'),
    path('ajax/guardar-respuestas/<int:curso_id>/<int:cuest_id>/', ajax_guardar_respuestas, name='ajax_guardar_respuestas'),
    path('curso/<int:curso_id>/ajax/caso/',views_ajax.ajax_caso_clinico,name='ajax_caso_clinico'),
    
    #Pasos de evaluacion de pacientes
    path('curso/<int:curso_id>/ajax/pasos/',views_ajax.ajax_guia_kine,name='ajax_guia_kine'),
    path('curso/<int:curso_id>/ajax/evaluaciones/',views_ajax.ajax_evaluaciones,name='ajax_evaluaciones'),
    path('curso/<int:curso_id>/ajax/cuestionario/<int:cuest_id>/guardar/',views_ajax.ajax_guardar_respuestas,name='ajax_guardar_respuestas'),


]


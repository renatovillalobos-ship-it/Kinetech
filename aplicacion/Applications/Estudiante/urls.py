from django.urls import path
from . import views
from . import views_videos
from . import views_ajax




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




]


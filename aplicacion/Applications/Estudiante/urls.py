from django.urls import path
from . import views
from . import views_videos




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




]


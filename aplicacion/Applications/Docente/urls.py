from django.urls import path
from . import views

app_name='docente'

urlpatterns = [
    path('home_docente/',views.Home_docente.as_view(),name='home_docente'),
    path('login/',views.Login.as_view(),name='login'),
    path('registro_docente/', views.RegistroDocente.as_view(), name='registro_docente'),
    path('autenticar/', views.AutenticarUsuario.as_view(), name='autenticar'),
    path('logout/', views.CerrarSesion.as_view(), name='logout'),


     # Rutas para la foto del docente
    
    path('perfil_docente/', views.PerfilDocente.as_view(), name='perfil_docente'),

    path('subir_foto/<int:id>/', views.subir_foto_docente, name='subir_foto_docente'),
    path('eliminar_foto/<int:id>/', views.eliminar_foto_docente, name='eliminar_foto_docente'),

    # RUtas para crear cursos automaticamente

    path('detalle_curso/<int:id>/', views.detalle_curso, name='detalle_curso'),


    #Rutas para progreso docente

    path('progreso/', views.ProgresoDocenteView.as_view(), name='progreso_docente'),
    path('progreso/<int:curso_id>/', views.ProgresoDocenteView.as_view(), name='progreso_curso'),
]
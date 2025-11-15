from django.urls import path
from . import views

urlpatterns = [
    path('home_docente/',views.Home_docente.as_view(),name='home_docente'),
    path('login/',views.Login.as_view(),name='login'),

     # Rutas para la foto del docente
    
    path('perfil_docente/', views.PerfilDocente.as_view(), name='perfil_docente'),

    path('subir_foto/<int:id>/', views.subir_foto_docente, name='subir_foto_docente'),
    path('eliminar_foto/<int:id>/', views.eliminar_foto_docente, name='eliminar_foto_docente'),

]
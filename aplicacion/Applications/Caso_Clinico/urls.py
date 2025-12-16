from django.urls import path
from . import views
from .views import VideoDetailView

app_name = 'Caso_Clinico'

urlpatterns = [
    path('lista/<int:curso_id>/', views.lista_casos_clinicos, name='lista_casos'),
    path('detalle/<int:caso_id>/', views.detalle_caso_clinico, name='detalle_caso'),
    path('seleccionar-paciente/<int:caso_id>/<int:parte_id>/', 
         views.seleccionar_paciente, name='seleccionar_paciente'),
    path('ver-etapas/<int:caso_id>/<int:parte_id>/<int:paciente_id>/', 
         views.ver_etapas, name='ver_etapas'),
    path('etapa-detalle/<int:caso_id>/<int:parte_id>/<int:paciente_id>/<int:etapa_id>/', 
         views.etapa_detalle, name='etapa_detalle'),
    
    # API endpoints
    path('api/opciones-tema/<int:tema_id>/', views.api_opciones_tema, name='api_opciones_tema'),
    path('procesar-respuesta/<int:caso_id>/<int:parte_id>/<int:paciente_id>/<int:etapa_id>/', 
         views.procesar_respuesta, name='procesar_respuesta'),
    path('progreso/<int:caso_id>/<int:parte_id>/<int:paciente_id>/', 
         views.ver_progreso, name='ver_progreso'),
     path("videos/<int:pk>/", VideoDetailView.as_view(), name="detalle_video"),
     path('api/diagnosticos/<int:etapa_id>/', views.api_diagnosticos, name='api_diagnosticos'),

]
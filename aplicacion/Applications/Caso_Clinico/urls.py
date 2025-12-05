from django.urls import path
from . import views

app_name = 'Caso_Clinico'

urlpatterns = [
    # Lista de casos por curso
    path('curso/<int:curso_id>/casos/', 
         views.lista_casos_clinicos, 
         name='casos_lista_casos'),
    
    # Detalle de caso
    path('casos/<int:caso_id>/', 
         views.detalle_caso_clinico, 
         name='detalle_caso'),
    
    # Seleccionar paciente
    path('casos/<int:caso_id>/parte/<int:parte_id>/', 
         views.seleccionar_paciente, 
         name='seleccionar_paciente'),
    
    # Ver etapas
    path('casos/<int:caso_id>/parte/<int:parte_id>/paciente/<int:paciente_id>/', 
         views.ver_etapas, 
         name='ver_etapas'),
]
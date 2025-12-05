from django.urls import path
from .views import ver_cuestionario

app_name = 'cuestionario'

urlpatterns = [
    path('curso/<int:curso_id>/cuestionario/', ver_cuestionario, name='cuestionario_lista'),
    path('curso/<int:curso_id>/cuestionario/<int:cuestionario_id>/', ver_cuestionario, name='cuestionario_detalle'),
]

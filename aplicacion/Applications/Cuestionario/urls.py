from django.urls import path
from . import views
from .views import ver_cuestionario


app_name = 'cuestionario'

urlpatterns = [
    path('cuestionario/<int:curso_id>/', ver_cuestionario, name='cuestionario')
]

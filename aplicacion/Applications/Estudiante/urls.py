from django.urls import path
from . import views

urlpatterns = [
    path('home_estudiante',views.Home_estudiante.as_view(),name='home_estudiante'),
]


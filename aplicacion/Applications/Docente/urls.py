from django.urls import path
from . import views

urlpatterns = [
    path('home_docente',views.Home_docente.as_view(),name='home_docente'),
    path('login',views.Login.as_view(),name='login')
]
from django.contrib import admin
from .models import *

class EstudianteAdmin(admin.ModelAdmin):
    list_display=(
        'nombre_estudiante',
        'apellido_estudiante',
        'correo_estudiante',
        'foto_perfil_estudiante',
        'pais_estudiante',
    )
    search_fields=('nombre_estudiante',)
# Register your models here.
admin.site.register(Estudiante,EstudianteAdmin)
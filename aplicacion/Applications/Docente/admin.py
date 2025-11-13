from django.contrib import admin
from .models import *

class DocenteAdmin(admin.ModelAdmin):
    list_display=(
        'nombre_docente',
        'correo_docente',
        'foto_perfil_docente',
        'pais_docente',
    )

# Register your models here.
admin.site.register(Docente,DocenteAdmin)
admin.site.register(Curso)
from django.contrib import admin
from .models import *

class DocenteAdmin(admin.ModelAdmin):
    list_display=(
        'nombre_docente',
        'apellido_docente',
        'correo_docente',
        'foto_perfil_docente',
        'pais_docente',
    )
    search_fields=('nombre_docente',)

class CursoAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'nombre_del_Curso',
        'fecha_realización_curso',
    )
    search_fields=('nombre_del_Curso',)
# Register your models here.
admin.site.register(Docente,DocenteAdmin)
admin.site.register(Curso,CursoAdmin)
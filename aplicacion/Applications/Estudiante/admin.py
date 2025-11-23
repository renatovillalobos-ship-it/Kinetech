from django.contrib import admin
from django.utils.html import format_html
from .models import *

class EstudianteAdmin(admin.ModelAdmin):
    list_display=(
        'nombre_estudiante',
        'apellido_estudiante',
        'correo_estudiante',
        'foto_preview',
        'pais_estudiante',
    )

    search_fields=('nombre_estudiante',)

    readonly_fields = ('foto_preview',) 

    filter_horizontal = ('cursos',)

    fieldsets = (
        (None, {
            'fields': (
                'nombre_estudiante',
                'apellido_estudiante',
                'correo_estudiante',
                'pais_estudiante',
                'cursos',
                'foto_perfil_estudiante',          
                'foto_preview',   
            )
        }),
    )

    def foto_preview(self, obj): 
        if obj.foto_perfil_estudiante:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 50%;" />',
                obj.foto_perfil_estudiante.url
            )
        return "Sin foto"
    foto_preview.short_description = "Foto de perfil"
# Register your models here.
admin.site.register(Estudiante,EstudianteAdmin)
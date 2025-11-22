from django.contrib import admin
from django.utils.html import format_html
from .models import *


class DocenteAdmin(admin.ModelAdmin):
    list_display=(
        'nombre_docente',
        'apellido_docente',
        'obtener_correo',
        'foto_preview',
        'pais_docente',
    )
    search_fields=('nombre_docente',)
    readonly_fields = ('foto_preview',) 
    fieldsets = (
        (None, {
            'fields': (
                'nombre_docente',
                'apellido_docente',
                'obtener_correo',
                'pais_docente', 
                'foto_perfil_docente',          
                'foto_preview',   
            )
        }),
    )

    def obtener_correo(self, obj):
        # Accede al campo email del objeto User vinculado
        return obj.user.email 

    obtener_correo.short_description = 'Correo Electrónico'

    def foto_preview(self, obj): 
        if obj.foto_perfil_docente:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 50%;" />',
                obj.foto_perfil_docente.url
            )
        return "Sin foto"
    foto_preview.short_description = "Foto de perfil"
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
from django.contrib import admin
from .models import *
# Register your models here.

class CuestionarioAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'nombre',
        'Curso__nombre_del_Curso',
    )
    search_fields = (
        'nombre', 
        'Curso__nombre_del_Curso',
    )
    
    list_filter = (
        'Curso__nombre_del_Curso',
        'Curso__fecha_realización_curso',
    )
    list_per_page = 20

class PreguntasAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'cuestionario__nombre',
        'enunciado',
    )
    search_fields = (
        'enunciado',
        'cuestionario__nombre',
    )

    list_filter = (
        'cuestionario__nombre',
    )
class RespuestaAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'ID_pregunta__enunciado',
        'es_correcta',
        'retro'
    )
    search_fields = (
        'ID_pregunta__enunciado',
        'retro',
    )
    list_filter = (
        'es_correcta',
    )
admin.site.register(cuestionario,CuestionarioAdmin)
admin.site.register(Preguntas,PreguntasAdmin)
admin.site.register(Respuesta,RespuestaAdmin)
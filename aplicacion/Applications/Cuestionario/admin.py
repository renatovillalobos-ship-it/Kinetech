from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import *


class PreguntasAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cuestionario__nombre',
        'enunciado',
    )
    search_fields = (
        'enunciado',
        'cuestionario__nombre',
    )
    list_filter = ('cuestionario__nombre',)

    # Limitar máximo 10 preguntas por cuestionario
    def save_model(self, request, obj, form, change):
        total = Preguntas.objects.filter(cuestionario=obj.cuestionario).count()
        if not change and total >= 10:
            raise ValidationError("⚠ Este cuestionario ya tiene 10 preguntas.")
        super().save_model(request, obj, form, change)


class RespuestaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ID_pregunta__enunciado',
        'es_correcta',
        'retro'
    )
    search_fields = (
        'ID_pregunta__enunciado',
        'retro',
    )
    list_filter = ('es_correcta',)

    # Limitar máximo 4 respuestas por pregunta
    def save_model(self, request, obj, form, change):
        total = Respuesta.objects.filter(ID_pregunta=obj.ID_pregunta).count()
        if not change and total >= 4:
            raise ValidationError("⚠ Esta pregunta ya tiene 4 respuestas.")
        super().save_model(request, obj, form, change)


class CuestionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'Curso__nombre_del_Curso')
    search_fields = ('nombre', 'Curso__nombre_del_Curso')
    list_filter = ('Curso__nombre_del_Curso', 'Curso__fecha_realización_curso')
    list_per_page = 20


admin.site.register(cuestionario, CuestionarioAdmin)
admin.site.register(Preguntas, PreguntasAdmin)
admin.site.register(Respuesta, RespuestaAdmin)

# admin.py - REEMPLAZA TODO EL CONTENIDO CON ESTO
from django.contrib import admin
from django import forms
from .models import *


class PacientesAdminForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = '__all__'
        widgets = {
            'prevision': forms.Select(attrs={'size': 6}),
        }


class PacientesAdmin(admin.ModelAdmin): 
    list_display = (
        'nombre',
        'fecha_nacimiento',
        'edad',
        'prevision',
        'ocupacion',
    )
    search_fields = ('nombre',)
    list_filter = ('fecha_nacimiento', 'edad', 'prevision', 'ocupacion')


class CasoClinicoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'caso',
        'Curso',
    )
    search_fields = ('caso', 'Curso__nombre_del_Curso')
    list_filter = ('Curso__nombre_del_Curso',)


class EtapaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'ParteCuerpo',
        'tipo',
        'orden',
        'tema',
    )
    search_fields = ('nombre', 'ParteCuerpo__ParteCuerpo', 'tema')
    list_filter = ('ParteCuerpo', 'tipo')
    list_editable = ('orden',)


class PartesCuerpoAdmin(admin.ModelAdmin): 
    list_display = (
        'id',
        'ParteCuerpo',
        'CasoClinico',
    )
    search_fields = ('ParteCuerpo', 'CasoClinico__caso')
    list_filter = ('CasoClinico__caso',)


class PreguntaEtapaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pregunta',
        'Etapa',
    )
    search_fields = ('pregunta', 'Etapa__nombre')
    list_filter = ('Etapa__nombre',)


class RespuestaEtapaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pregunta',
        'texto',
        'correcta',
    )
    search_fields = ('texto', 'retroalimentacion', 'pregunta__pregunta')
    list_filter = ('correcta', 'pregunta__Etapa__nombre')


class TemaConsultaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'etapa', 'orden', 'icono')
    list_filter = ('etapa',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('orden',)


class OpcionTemaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'tema', 'es_correcta', 'lleva_a_etapa')
    list_filter = ('es_correcta', 'tema__etapa')
    search_fields = ('texto', 'retroalimentacion')


class PartesPacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'Pacientes', 'ParteCuerpo')
    list_filter = ('ParteCuerpo',)
    search_fields = ('Pacientes__nombre', 'ParteCuerpo__ParteCuerpo')


# Register your models here UNA SOLA VEZ
admin.site.register(Pacientes, PacientesAdmin)
admin.site.register(Caso_clinico, CasoClinicoAdmin)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(Partes_paciente, PartesPacienteAdmin)
admin.site.register(Partes_cuerpo, PartesCuerpoAdmin)
admin.site.register(PreguntaEtapa, PreguntaEtapaAdmin)
admin.site.register(RespuestaEtapa, RespuestaEtapaAdmin)
admin.site.register(TemaConsulta, TemaConsultaAdmin)
admin.site.register(OpcionTema, OpcionTemaAdmin)
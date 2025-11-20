from django.contrib import admin
from django import forms
from .models import *

class PacientesAdminForm(forms.ModelForm): #Para mostrar lista desplegable hacia abajo :)
    class Meta:
        model = Pacientes
        fields = '__all__'
        widgets = {
            'prevision': forms.Select(attrs={'size': 6}),
        }
class PacientesAdmin(admin.ModelAdmin): 
    list_display=(
        'nombre',
        'fecha_nacimiento',
        'edad',
        'prevision',
        'ocupacion',
    )
    search_fields=('nombre',)
    list_filter = ('fecha_nacimiento', 'edad','prevision','ocupacion',)

class CasoClinicoAdmin(admin.ModelAdmin):
    list_display=(
        'Curso__id',
        'Curso__fecha_realización_curso',
        'Curso__nombre_del_Curso',
        'caso',
    )
    search_fields = ('caso', 'Curso__nombre_del_Curso') 
    
    list_filter = ('Curso__nombre_del_Curso', 'Curso__fecha_realización_curso')

class EtapaAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'nombre',
        'ParteCuerpo',

    )
    search_fields=('nombre',)

    list_filter = ('ParteCuerpo',)

class PartesCuerpoAdmin(admin.ModelAdmin): 
    list_display=(
        'id',
        'ParteCuerpo',
        'CasoClinico__caso',

    )
    search_fields = ('ParteCuerpo', 'CasoClinico__caso')

    list_filter = ('CasoClinico__caso',)

class PreguntaEtapaAdmin(admin.ModelAdmin):
    list_display=(

        'id',
        'Etapa__nombre',
        'pregunta',

    )
    search_fields = ('pregunta', 'Etapa__nombre')

    list_filter = ('Etapa__nombre',)

class RespuestaEtapaAdmin(admin.ModelAdmin):
    list_display=(

        'id',
        'pregunta__Etapa__nombre',
        'pregunta__pregunta',
        'retroalimentacion',
        'correcta',
    )
    search_fields = ('pregunta__pregunta', 'retroalimentacion')
    
    list_filter = ('correcta', 'pregunta__Etapa__nombre')
# Register your models here.
admin.site.register(Pacientes,PacientesAdmin)
admin.site.register(Caso_clinico,CasoClinicoAdmin)
admin.site.register(Etapa,EtapaAdmin)
admin.site.register(Partes_paciente)
admin.site.register(Partes_cuerpo,PartesCuerpoAdmin)
admin.site.register(PreguntaEtapa,PreguntaEtapaAdmin)
admin.site.register(RespuestaEtapa,RespuestaEtapaAdmin)
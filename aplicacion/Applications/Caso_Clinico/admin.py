from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Pacientes)
admin.site.register(Caso_clinico)
admin.site.register(Etapa)
admin.site.register(Partes_paciente)
admin.site.register(Partes_cuerpo)
admin.site.register(RespuestaEtapa)
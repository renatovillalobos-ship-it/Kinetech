from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(cuestionario)
admin.site.register(Tipo_Respuesta)
admin.site.register(Preguntas)
admin.site.register(Respuesta)
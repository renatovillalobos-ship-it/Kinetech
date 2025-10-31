from django.db import models
from Applications.Docente.models import Curso

# Create your models here.
class cuestionario(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre=models.CharField('Nombre Cuestionario',max_length=100, null=False)

    def __str__(self):
        return str(self.id)+'-'+self.nombre


class Tipo_Respuesta(models.Model):
    tipo = models.CharField(max_length=50, choices=[('Abierta', 'Abierta'), ('Cerrada', 'Cerrada')])


    def __str__(self):
        return str(self.id) + '-' + self.tipo


class Preguntas(models.Model):
    cuestionario = models.ForeignKey(cuestionario, on_delete=models.CASCADE)
    enunciado = models.TextField('Enunciado Pregunta', null=False )
    tipo_respuesta = models.ForeignKey(Tipo_Respuesta, on_delete=models.CASCADE)

    
    def __str__(self):
        return str(self.id)+'-'+self.enunciado


class Respuesta(models.Model):
    es_correcta = models.BooleanField(default=False)
    retro = models.TextField('Retroalimentación', null=False)
    ID_pregunta = models.ForeignKey(Preguntas,on_delete=models.CASCADE)
   
    def __str__(self):
        return self.id + '-' + self.es_correcta + '-' + self.retro


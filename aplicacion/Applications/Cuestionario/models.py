from django.db import models
from Applications.Docente.models import Curso

# Create your models here.
class cuestionario(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre=models.CharField('Nombre Cuestionario',max_length=100, null=False)

    def __str__(self):
        return str(self.id)+'-'+self.nombre

class Preguntas(models.Model):
    cuestionario = models.ForeignKey(cuestionario, on_delete=models.CASCADE)
    enunciado = models.TextField('Enunciado Pregunta', null=False )

    
    def __str__(self):
        return str(self.id)+'-'+self.enunciado



from django.db import models
from django.core.exceptions import ValidationError

from Applications.Docente.models import Curso


# Create your models here.
class cuestionario(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre=models.CharField('Nombre Cuestionario',max_length=100, null=False)

    class Meta:
        verbose_name='Cuestionario'
        verbose_name_plural='Cuestionarios'
        ordering=['id']

    def __str__(self):
        return str(self.id)+'-'+self.nombre

class Preguntas(models.Model):
    cuestionario = models.ForeignKey(cuestionario, on_delete=models.CASCADE)
    enunciado = models.TextField('Enunciado Pregunta', null=False )

    class Meta:
        verbose_name='Pregunta'
        verbose_name_plural='Preguntas'
        ordering=['id','enunciado']


    def clean(self):
        if Preguntas.objects.filter(cuestionario=self.cuestionario).exclude(id=self.id).count() >= 10:
            raise ValidationError("⚠ Este cuestionario ya tiene 10 preguntas.")
        
    def save(self, *args, **kwargs):
        self.clean()  # forza la validación antes de guardar
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)+'-'+self.enunciado


class Respuesta(models.Model):
    ID_pregunta = models.ForeignKey(Preguntas,on_delete=models.CASCADE)
    es_correcta = models.BooleanField(default=False)
    retro = models.TextField('Retroalimentación', null=False)

    class Meta:
        verbose_name='Respuesta'
        verbose_name_plural='Respuestas'
        ordering=['id']

    def clean(self):
        if Respuesta.objects.filter(ID_pregunta=self.ID_pregunta).exclude(id=self.id).count() >= 4:
            raise ValidationError("⚠ Esta pregunta ya tiene 4 respuestas.")
   
    def save(self, *args, **kwargs):
        self.clean()  # forza la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)  + '-' + self.retro
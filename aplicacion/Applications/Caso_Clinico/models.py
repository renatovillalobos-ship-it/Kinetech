from django.db import models
from Applications.Docente.models import Curso
# Create your models here.

class Pacientes(models.Model):
    fecha_nacimiento=models.DateField('Fecha de Nacimiento', null=False)
    nombre=models.CharField('Nombre Paciente', max_length=100, null=False)
    
    def __str__(self):
        return str(self.id)+'-'+self.nombre
    
class Caso_clinico(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    caso=models.CharField('Nombre Caso', max_length=100, null=False)
    def __str__(self):
        return str(self.id)+'-'+self.caso
    
class Etapa(models.Model):
    nombre=models.CharField('Nombre Etapa', max_length=50, null=False)
    video=models.URLField()
    pregunta=models.CharField('Pregunta Etapa', max_length=150, null=False)
    Caso_clinico = models.ForeignKey(Caso_clinico, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+self.nombre
    
class EtapaPaciente(models.Model):
    Pacientes = models.ForeignKey(Pacientes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+self.Pacientes

class Partes_cuerpo(models.Model):
    ParteCuerpo =models.CharField('Parte del cuerpo', max_length=100, null=False)
    Etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+self.ParteCuerpo
    
class RespuestaEtapa(models.Model):
    retroalimentacion=models.CharField('Retroalimentación', max_length=200, null=False)
    correcta=models.BooleanField('Correcta')
    Etapa=models.ForeignKey(Etapa, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+self.retroalimentacion
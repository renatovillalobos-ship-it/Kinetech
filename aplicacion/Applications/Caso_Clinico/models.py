from django.db import models
from Applications.Docente.models import Curso
# Create your models here.

class Pacientes(models.Model):
    fecha_nacimiento=models.DateField('Fecha de Nacimiento', null=False)
    nombre=models.CharField('Nombre Paciente', max_length=100, null=False)
    #imagen
    
    def __str__(self):
        return str(self.id)+'-'+self.nombre

class Caso_clinico(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    caso=models.CharField('Nombre Caso', max_length=100, null=False)
    #ParteCuerpo =models.CharField('Parte del cuerpo', max_length=100, null=False)
    #Etapa = models.ForeignKey('Etapa', on_delete=models.CASCADE)
    #Paciente = models.ForeignKey(Pacientes,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)+'-'+self.caso

class Partes_cuerpo(models.Model):
    ParteCuerpo =models.CharField('Parte del cuerpo', max_length=100, null=False)
    CasoClinico = models.ForeignKey(Caso_clinico, on_delete=models.CASCADE)
    #Paciente = models.ForeignKey(Pacientes,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+str(self.ParteCuerpo)  

class Partes_paciente(models.Model):
    Pacientes = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    ParteCuerpo = models.ForeignKey(Partes_cuerpo,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+str(self.Pacientes)+'-'+str(self.ParteCuerpo)
    

class Etapa(models.Model):
    ParteCuerpo = models.ForeignKey(Partes_cuerpo, on_delete=models.CASCADE)
    nombre=models.CharField('Nombre Etapa', max_length=50, null=False)
    pregunta=models.CharField('Pregunta Etapa', max_length=150, null=True, blank=True)
    video=models.URLField(null=True, blank=True)
    #Caso_clinico = models.ForeignKey('Caso_clinico', on_delete=models.CASCADE)
    #Paciente = models.ForeignKey(Pacientes,on_delete=models.CASCADE)

    def __str__(self):
        pregunta_str = self.pregunta or 'Sin Pregunta' 
        return str(self.id) + '-' + pregunta_str +  '-' + self.nombre

    
class RespuestaEtapa(models.Model):
    retroalimentacion=models.CharField('Retroalimentación', max_length=200, null=False)
    correcta=models.BooleanField('Correcta')
    Etapa=models.ForeignKey(Etapa, on_delete=models.CASCADE)
    def __str__(self):
        etapa = self.Etapa 
        
        pregunta_str = etapa.pregunta or 'Sin Pregunta'

        return str(self.id) +  '-' +  self.retroalimentacion + '-' +  pregunta_str
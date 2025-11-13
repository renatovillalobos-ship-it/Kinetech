from django.db import models
from Applications.Docente.models import Curso
# Create your models here.

class Pacientes(models.Model):
    fecha_nacimiento=models.DateField('Fecha de Nacimiento', null=False)
    nombre=models.CharField('Nombre Paciente', max_length=100, null=False)
    edad=models.IntegerField('Edad Paciente',null=False)
    prevision=models.CharField('Previsión',max_length=50,null=False)
    ocupacion=models.CharField('Ocupación',max_length=100,null=False)

    #imagen
    class Meta: 
        verbose_name='Paciente'
        verbose_name_plural='Pacientes'
        ordering=['fecha_nacimiento','nombre']

    def __str__(self):
        return str(self.id)+'-'+self.nombre

class Caso_clinico(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    caso=models.CharField('Nombre Caso', max_length=100, null=False)
    #ParteCuerpo =models.CharField('Parte del cuerpo', max_length=100, null=False)
    #Etapa = models.ForeignKey('Etapa', on_delete=models.CASCADE)
    #Paciente = models.ForeignKey(Pacientes,on_delete=models.CASCADE)
    class Meta:
        verbose_name='Caso clínico'
        verbose_name_plural='Casos clínicos'

    def __str__(self):
        return str(self.id)+'-'+self.caso

class Partes_cuerpo(models.Model):
    ParteCuerpo =models.CharField('Parte del cuerpo', max_length=100, null=False)
    CasoClinico = models.ForeignKey(Caso_clinico, on_delete=models.CASCADE)
    #Paciente = models.ForeignKey(Pacientes,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Parte del cuerpo'
        verbose_name_plural='Partes del cuerpo'
        unique_together=('ParteCuerpo','CasoClinico')

    def __str__(self):
        return str(self.id)+'.'+str(self.ParteCuerpo)  

class Partes_paciente(models.Model):
    Pacientes = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    ParteCuerpo = models.ForeignKey(Partes_cuerpo,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+str(self.Pacientes)+'-'+str(self.ParteCuerpo)
    

class Etapa(models.Model):
    ParteCuerpo = models.ForeignKey(Partes_cuerpo, on_delete=models.CASCADE)
    nombre=models.CharField('Nombre Etapa', max_length=50, null=False)
    #pregunta=models.CharField('Pregunta Etapa', max_length=150, null=True, blank=True)
    video=models.URLField(null=True, blank=True)
    #Caso_clinico = models.ForeignKey('Caso_clinico', on_delete=models.CASCADE)
    #Paciente = models.ForeignKey(Pacientes,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Etapa'
        verbose_name_plural='Etapas'
        ordering=['nombre','ParteCuerpo']

    def __str__(self):
        return str(self.id) + '-' + '-' + self.nombre

    
class PreguntaEtapa(models.Model):
    Etapa=models.ForeignKey(Etapa, on_delete=models.CASCADE)
    pregunta=models.CharField('Pregunta Etapa', max_length=150, null=True, blank=True)

    class Meta:
        verbose_name='Pregunta etapa'
        verbose_name_plural='Preguntas etapa'
        ordering=['id','Etapa']

    def __str__(self):
        return str(self.id) + '-' + self.Etapa.nombre + '-'+ self.pregunta

class RespuestaEtapa(models.Model):
    #Etapa=models.ForeignKey(Etapa, on_delete=models.CASCADE)
    pregunta=models.ForeignKey(PreguntaEtapa,on_delete=models.CASCADE)
    retroalimentacion=models.CharField('Retroalimentación', max_length=200, null=False)
    correcta=models.BooleanField('Correcta')

    class Meta:
        verbose_name='Respuesta etapa'
        verbose_name_plural='Respuestas etapa'
        ordering=['id','pregunta']

    def __str__(self):

        return str(self.id) +  '-' +  self.retroalimentacion + '-' + ' Pregunta: ' + self.pregunta.pregunta
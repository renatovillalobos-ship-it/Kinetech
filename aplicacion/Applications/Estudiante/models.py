from django.db import models
from Applications.Docente.models import Curso
from Applications.Docente.models import Docente


# Create your models here.
class Estudiante(models.Model):
    nombre_estudiante= models.CharField('Nombre Estudiante', max_length=150, null=False)
    apellido_estudiante= models.CharField('Apellido Estudiante', max_length=150, null=False)
    correo_estudiante= models.EmailField('Correo Electronico', unique=True)
    pais_estudiante = models.CharField('País Estudiante', max_length=150, null=False)
    foto_perfil_estudiante= models.ImageField(
    'Foto perfil estudiante', 
    upload_to='perfiles/estudiantes/', # 'perfiles/estudiantes/' se creará DENTRO de la nueva carpeta 'media'
    null=True, blank=True
)
    contrasena_estudiante = models.CharField('Contraseña Estudiante', max_length=150)
    curso_estudiante= models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name='Estudiante'
        verbose_name_plural='Estudiantes'
        ordering=['apellido_estudiante','nombre_estudiante']

    def __str__(self):
        return self.nombre_estudiante + '-'+self.apellido_estudiante



class Progreso(models.Model):
    fecha_progreso_inicial = models.DateField('Fecha de Progreso de Inicio')
    fecha_progreso_termino = models.DateField('Fecha de Progreso de Termino')
    puntaje_obtenido_inicial= models.FloatField()
    puntaje_obtenido_final= models.FloatField()
    porcentaje_progreso= models.DecimalField(max_digits=10, decimal_places=2)
    progreso_curso= models.ForeignKey(Curso, on_delete=models.CASCADE)
    progreso_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    docente_Correspondiente_progreso = models.ForeignKey(Docente, on_delete=models.CASCADE)

    def __str__(self):
         return str(self.id) + '-' + self.porcentaje_progreso  + '-' +  self.progreso_estudiante
    


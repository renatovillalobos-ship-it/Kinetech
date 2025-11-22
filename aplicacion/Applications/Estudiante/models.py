from django.db import models
from Applications.Docente.models import Curso
from Applications.Docente.models import Docente
from Applications.Caso_Clinico.models import Partes_cuerpo, Etapa  
from django.core.validators import RegexValidator #Validador de letras y números

solo_letras = RegexValidator(
    r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]*$', # Patrón permitido
    'Este campo solo puede contener letras y espacios.' # Mensaje de error
)
# Create your models here.
class Estudiante(models.Model):

    pais_opciones = [('Chile', 'Chile'),
                     ('Argentina','Argentina'),
                     ('Brasil', 'Brasil'),
                     ('Peru','Peru'),
                     ('Otro', 'Otro')]
    nombre_estudiante= models.CharField('Nombre Estudiante', 
                                        max_length=150, 
                                        null=False,
                                        validators=[solo_letras])
    apellido_estudiante= models.CharField('Apellido Estudiante', 
                                          max_length=150, 
                                          null=False,
                                          validators=[solo_letras])
    correo_estudiante= models.EmailField('Correo Electronico', unique=True)
    pais_estudiante = models.CharField('País Estudiante', 
                                       max_length=150, 
                                       null=False,
                                       choices=pais_opciones,
                                       default='Chile')
    foto_perfil_estudiante= models.ImageField(
    'Foto perfil estudiante', 
    upload_to='perfiles/estudiantes/', # 'perfiles/estudiantes/' se creará DENTRO de la nueva carpeta 'media'
    null=True, blank=True
)
    contrasena_estudiante = models.CharField('Contraseña Estudiante', max_length=150)
    curso_estudiante= models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)

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
    
    # NUEVOS CAMPOS para tracking de videos
    parte_cuerpo = models.ForeignKey(Partes_cuerpo, on_delete=models.CASCADE, null=True, blank=True)
    etapa_completada = models.ForeignKey(Etapa, on_delete=models.CASCADE, null=True, blank=True)
    video_visto = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Progreso'
        verbose_name_plural = 'Progresos'

    def __str__(self):
        return f"{self.id} - {self.porcentaje_progreso}% - {self.progreso_estudiante}"

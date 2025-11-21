from django.db import models
#from Applications.Administrador.models import Administrador
from django.core.exceptions import ValidationError
from PIL import Image

from django.core.validators import RegexValidator #Validador de letras y números

# Create your models here.

solo_letras = RegexValidator(
    r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]*$', # Patrón permitido
    'Este campo solo puede contener letras y espacios.' # Mensaje de error
)


def validacion_imagen(value):
    if not value.name.lower().endswith('.png'):
        raise ValidationError("La imagen debe ser formato PNG.")
    try:
        imagen = Image.open(value)
        if imagen.format != 'PNG':
            raise ValidationError("El archivo NO es un PNG real. Debe ser una imagen PNG.")
    except Exception:
        raise ValidationError("Archivo inválido. Debe ser una imagen PNG.")
    
class Docente(models.Model):
    pais_opciones = [('CL', 'Chile'),
                     ('AR','Argentina'),
                     ('BR', 'Brasil'),
                     ('PE','Peru'),
                     ('OTRO', 'Otro')]
    
    nombre_docente = models.CharField('Nombre Docente', 
                                      max_length=150, 
                                      null=False,
                                      validators=[solo_letras])
    apellido_docente = models.CharField('Apellido Docente', 
                                        max_length=150, 
                                        null=False,
                                        validators=[solo_letras])
    asignatura_docente = models.CharField('Asignatura', max_length=150, null=False)
    pais_docente = models.CharField('País Docente', 
                                    max_length=150, 
                                    null=False,
                                    choices=pais_opciones,
                                    default='Chile')
    foto_perfil_docente = models.ImageField(
    'Foto perfil docente', 
    upload_to='perfiles/docentes/', # 'perfiles/estudiantes/' se creará DENTRO de la nueva carpeta 'media'
    validators=[validacion_imagen],
    null=True, blank=True
)
    correo_docente = models.EmailField('Correo electronico', unique=True)
    contrasena_docente = models.CharField('Contraseña', max_length=150)

    class Meta:
        verbose_name='Docente'
        verbose_name_plural='Docentes'
        ordering=['apellido_docente', 'nombre_docente']


    def __str__(self):
        return  self.nombre_docente + ' '+ self.apellido_docente


class Curso(models.Model):
    nombre_del_Curso = models.CharField('Nombre del Curso', max_length=150, null=False)
    Descripcion_del_curso = models.TextField('Descripción del Curso', max_length=150, null=False)
    fecha_realización_curso = models.DateField('Fecha Realización Curso')
    paralelo_curso= models.IntegerField('Paralelo Curso', null=False)
    curso_docente = models.ForeignKey(Docente, on_delete=models.CASCADE)

    class Meta: 
        verbose_name='Curso'
        verbose_name_plural='Cursos'
        ordering=['fecha_realización_curso', 'nombre_del_Curso']

    def __str__(self):
        return str(self.id) + '-' + self.nombre_del_Curso + ' ' + str(self.fecha_realización_curso)
    



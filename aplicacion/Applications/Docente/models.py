from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

solo_letras = RegexValidator(
    r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]*$',
    'Este campo solo puede contener letras y espacios.'
)

def validacion_imagen(value):
    ext = value.name.split('.')[-1].lower()
    
    formatos_validos = ['png', 'jpg', 'jpeg']
    
    if ext not in formatos_validos:
        raise ValidationError("La imagen debe ser PNG, JPG o JPEG.")
    
    try:
        img = Image.open(value)
        img.verify()
    except Exception:
        raise ValidationError("El archivo no es una imagen válida.")
    
class Curso(models.Model):
    nombre_del_Curso = models.CharField('Nombre del Curso', max_length=150, null=False)
    Descripcion_del_curso = models.TextField('Descripción del Curso', max_length=1000, null=False)
    Descripcion_breve_del_curso=models.TextField('Breve Descripción', max_length=150, null=False)
    fecha_realización_curso = models.DateField('Fecha Realización Curso')
    paralelo_curso= models.IntegerField('Paralelo Curso', null=False)

    class Meta: 
        verbose_name='Curso'
        verbose_name_plural='Cursos'
        ordering=['fecha_realización_curso', 'nombre_del_Curso']

    def __str__(self):
        return str(self.id) + '-' + self.nombre_del_Curso + ' ' + str(self.fecha_realización_curso)
    
User = get_user_model()

class Docente(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    curso_principal = models.ForeignKey(Curso, on_delete=models.SET_NULL, 
                                        null=True, blank=True,default=None, related_name='docentes')
    foto_perfil_docente = models.ImageField(
    'Foto perfil docente', 
    upload_to='perfiles/docentes/',
    validators=[validacion_imagen],
    null=True, blank=True
)

    class Meta:
        verbose_name='Docente'
        verbose_name_plural='Docentes'
        ordering=['apellido_docente', 'nombre_docente']

    def save(self, *args, **kwargs):
        if self.curso_principal:
            self.asignatura_docente = self.curso_principal.nombre_del_Curso
        super().save(*args, **kwargs)

    def __str__(self):
        return  self.nombre_docente + ' '+ self.apellido_docente


    



from django.db import models
#from Applications.Administrador.models import Administrador

# Create your models here.
class Docente(models.Model):
    nombre_docente = models.CharField('Nombre Docente', max_length=150, null=False)
    apellido_docente = models.CharField('Apellido Docente', max_length=150, null=False)
    asignatura_docente = models.CharField('Asignatura', max_length=150, null=False)
    pais_docente = models.CharField('País Docente', max_length=150, null=False)
    foto_perfil_docente = models.ImageField(
    'Foto perfil docente', 
    upload_to='perfiles/docentes/', # 'perfiles/estudiantes/' se creará DENTRO de la nueva carpeta 'media'
    null=True, blank=True
)
    correo_docente = models.EmailField('Correo electronico', unique=True)
    contrasena_docente = models.CharField('Contraseña', max_length=150)


    def __str__(self):
        return str(self.id)+ '-' + self.nombre_docente + '-'+ self.apellido_docente


class Curso(models.Model):
    nombre_del_Curso = models.CharField('Nombre del Curso', max_length=150, null=False)
    Descripcion_del_curso = models.TextField('Descripción del Curso', max_length=150, null=False)
    fecha_realización_curso = models.DateField('Fecha Realización Curso')
    paralelo_curso= models.CharField('Paralelo Curso', max_length=10, null=False)
    curso_docente = models.ForeignKey(Docente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + '-' + self.nombre_del_Curso + '-' + str(self.fecha_realización_curso)
    



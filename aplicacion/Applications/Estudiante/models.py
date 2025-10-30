from django.db import models
#from Applications.Docente.models import Curso


# Create your models here.
class Estudiante(models.Model):
    nombre_estudiante= models.CharField('Nombre Estudiante', max_length=150, null=False)
    apellido_estudiante= models.CharField('Apellido_Estudiante', max_length=150, null=False)
    correo_estudiante= models.EmailField('Correo Electronico', unique=True)
    pais_estudiante = models.CharField('País Docente', max_length=150, null=False)
    foto_perfil_estudiante= models.Field()
    contrasena_estudiante = models.CharField('Contraseña Estudiante', max_length=150)
    #curso_estudiante= models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+ self.nombre_estudiante + '-'+self.apellido_estudiante

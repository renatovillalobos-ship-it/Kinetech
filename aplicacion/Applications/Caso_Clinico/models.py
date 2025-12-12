from django.db import models
from django.forms import ValidationError
from Applications.Docente.models import Curso
from django.core.validators import RegexValidator
from datetime import datetime  # Añade este import

solo_letras = RegexValidator(
    r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]*$',
    'Este campo solo puede contener letras y espacios.'
)


class Pacientes(models.Model):
    prevision_opciones = [
        ('Fonasa', 'Fonasa'),
        ('Isapre', 'Isapre'),
        ('Particular', 'Particular/Privado'),
        ('Otro', 'Otro'),
        ('No aplica', 'No aplica')
    ]
    
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=False)
    nombre = models.CharField('Nombre Paciente', max_length=100, null=False)
    edad = models.IntegerField('Edad Paciente', null=False)
    ocupacion = models.CharField(
        'Ocupación',
        max_length=100,
        null=False,
        validators=[solo_letras]
    )
    prevision = models.CharField(
        'Previsión',
        max_length=50,
        null=False,
        choices=prevision_opciones,
        default='Fonasa'
    )
    
    class Meta: 
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['fecha_nacimiento', 'nombre']
    
    def __str__(self):
        return f"{self.id}-{self.nombre}"


class Caso_clinico(models.Model):
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    caso = models.CharField('Nombre Caso', max_length=100, null=False)
    
    class Meta:
        verbose_name = 'Caso clínico'
        verbose_name_plural = 'Casos clínicos'
    
    def __str__(self):
        return f"{self.id}-{self.caso}"


class Partes_cuerpo(models.Model):
    ParteCuerpo = models.CharField(
        'Parte del cuerpo', 
        max_length=100, 
        null=False,
        validators=[solo_letras] 
    )
    CasoClinico = models.ForeignKey(Caso_clinico, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Parte del cuerpo'
        verbose_name_plural = 'Partes del cuerpo'
        unique_together = ('ParteCuerpo', 'CasoClinico')
    
    def __str__(self):
        return f"{self.id}.{self.ParteCuerpo}"


class Partes_paciente(models.Model):
    Pacientes = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    ParteCuerpo = models.ForeignKey(Partes_cuerpo, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Relación Paciente-Parte'
        verbose_name_plural = 'Relaciones Paciente-Parte'
    
    def __str__(self):
        return f"{self.id}-{self.Pacientes.nombre}-{self.ParteCuerpo.ParteCuerpo}"


class Etapa(models.Model):
    TIPO_CHOICES = [
        ('video_inicial', 'Video Inicial'),
        ('formulario_temas', 'Formulario de Temas'),
        ('tratamientos', 'Tratamientos'),
        ('diagnosticos', 'Diagnósticos'),
    ]
    
    ParteCuerpo = models.ForeignKey(Partes_cuerpo, on_delete=models.CASCADE)
    nombre = models.CharField('Nombre Etapa', max_length=100, null=False)
    tipo = models.CharField('Tipo de Etapa', max_length=20, choices=TIPO_CHOICES, default='video_inicial')
    video = models.URLField('URL del Video', null=True, blank=True)
    orden = models.IntegerField('Orden', default=1)
    
    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        ordering = ['ParteCuerpo', 'orden']
        unique_together = ['ParteCuerpo', 'orden']
    
    def __str__(self):
        return f"{self.ParteCuerpo.ParteCuerpo} - {self.nombre} ({self.get_tipo_display()})"

    def clean(self):
        super().clean()
        if self.video and self.tipo in ['video_inicial']:

            if 'youtube.com' not in self.video and 'youtu.be' not in self.video:
                raise ValidationError('Solo se permiten URLs de YouTube para videos.')
            
            if not self.embed_url():

                raise ValidationError(
                    'La URL de YouTube no tiene un formato válido (watch?v= o youtu.be/). '
                    'Por favor, revise la URL.'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def tiene_video_valido(self):
        """Verifica si el video es válido"""
        if not self.video:
            return False
        return 'youtube.com' in self.video or 'youtu.be' in self.video
    
    def embed_url(self):
        """Genera URL embed para el video de respuesta"""
        if not self.video:
            return ""
        
        try:
            video_id = ""
            url = self.video
            
            if '/shorts/' in url:
                video_id = url.split('/shorts/')[1].split('?')[0][:11]
            
            # Caso 2: Enlaces youtu.be
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1].split('?')[0][:11]
            
            # Caso 3: Enlaces watch?v=
            elif 'watch?v=' in url:
                video_id = url.split('watch?v=')[1].split('&')[0][:11]
            
            # Caso 4: Enlaces embed/
            elif 'embed/' in url:
                video_id = url.split('embed/')[1].split('?')[0][:11]
            
            # Caso 5: Enlaces youtu.be con shorts (alternativo)
            elif 'youtu.be/shorts/' in url:
                video_id = url.split('youtu.be/shorts/')[1].split('?')[0][:11]
            
            if len(video_id) == 11:
                return f"https://www.youtube.com/embed/{video_id}?rel=0"
            return ""
        except Exception:
            return ""

class TemaConsulta(models.Model):
    """Temas que se pueden evaluar en el formulario de temas"""
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='temas', 
                              limit_choices_to={'tipo': 'formulario_temas'})
    nombre = models.CharField('Nombre del Tema', max_length=100)
    descripcion = models.TextField('Descripción', blank=True)
    orden = models.IntegerField('Orden', default=1)
    
    class Meta:
        ordering = ['etapa', 'orden']
        verbose_name = 'Tema de Consulta'
        verbose_name_plural = 'Temas de Consulta'
    
    def __str__(self):
        return f"{self.nombre} - {self.etapa.nombre}"

class OpcionTema(models.Model):
    tema = models.ForeignKey(TemaConsulta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.TextField('Pregunta')
    es_correcta = models.BooleanField('Es correcta', default=False)
    retroalimentacion = models.TextField('Retroalimentación', blank=True)
    video_respuesta = models.URLField('Video de respuesta correcta', blank=True, null=True,
                                     help_text="URL de YouTube para respuesta correcta")
    
    class Meta:
        verbose_name = 'Opción de Tema'
        verbose_name_plural = 'Opciones de Tema'
    
    def __str__(self):
        return f"{self.texto[:50]}... ({'✓' if self.es_correcta else '✗'})"
    
    def embed_url(self):
        """Genera URL embed para el video de respuesta"""
        if not self.video_respuesta:
            return ""
        
        try:
            video_id = ""
            url = self.video_respuesta
            
            # Caso 1: YouTube Shorts (como en la imagen: https://youtube.com/shorts/fMjFxdEGbQk?feature=share)
            if '/shorts/' in url:
                video_id = url.split('/shorts/')[1].split('?')[0][:11]
            
            # Caso 2: Enlaces youtu.be
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1].split('?')[0][:11]
            
            # Caso 3: Enlaces watch?v=
            elif 'watch?v=' in url:
                video_id = url.split('watch?v=')[1].split('&')[0][:11]
            
            # Caso 4: Enlaces embed/
            elif 'embed/' in url:
                video_id = url.split('embed/')[1].split('?')[0][:11]
            
            # Caso 5: Enlaces youtu.be con shorts (alternativo)
            elif 'youtu.be/shorts/' in url:
                video_id = url.split('youtu.be/shorts/')[1].split('?')[0][:11]
            
            if len(video_id) == 11:
                return f"https://www.youtube.com/embed/{video_id}?rel=0"
            return ""
        except Exception:
            return ""
        
class Diagnostico_Tratamiento(models.Model):

    TIPO_CONTENIDO = [
        ('diagnostico', 'Diagnóstico'),
        ('tratamiento', 'Tratamiento'),
    ]
    
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='contenidos', limit_choices_to={
            'tipo__in': ['diagnosticos', 'tratamientos']
        })
    tipo = models.CharField('Tipo de contenido', max_length=20, choices=TIPO_CONTENIDO)
    titulo = models.CharField('Título', max_length=200)
    descripcion = models.TextField('Descripción')
    orden = models.IntegerField('Orden', default=1)
    
    class Meta:
        ordering = ['etapa', 'orden']
        verbose_name = 'Diagnóstico y tratamiento'
        verbose_name_plural = 'Diagnósticos y tratamientos'
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo}"
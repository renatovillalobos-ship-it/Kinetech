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
        ('preguntas_tema', 'Preguntas sobre Tema'),
        ('video_respuesta', 'Video de Respuesta'),
        ('tratamientos', 'Tratamientos'),
        ('diagnosticos', 'Diagnósticos'),
    ]
    
    ParteCuerpo = models.ForeignKey(Partes_cuerpo, on_delete=models.CASCADE)
    nombre = models.CharField('Nombre Etapa', max_length=100, null=False)
    tipo = models.CharField('Tipo de Etapa', max_length=20, choices=TIPO_CHOICES, default='video_inicial')
    video = models.URLField('URL del Video', null=True, blank=True)
    tema = models.CharField('Tema específico', max_length=100, blank=True, null=True)
    orden = models.IntegerField('Orden', default=1)
    
    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        ordering = ['ParteCuerpo', 'orden']
        unique_together = ['ParteCuerpo', 'orden']
    
    def __str__(self):
        return f"{self.ParteCuerpo.ParteCuerpo} - {self.nombre} ({self.get_tipo_display()})"
    
# models.py - En la clase Etapa

    def clean(self):
        super().clean()
        if self.video and self.tipo in ['video_inicial', 'video_respuesta']:
            # Validar que la URL sea de YouTube
            if 'youtube.com' not in self.video and 'youtu.be' not in self.video:
                raise ValidationError('Solo se permiten URLs de YouTube para videos.')
            
            # Validación Adicional: Intentar generar el embed URL para asegurar que la URL es parseable
            if not self.embed_url():
                # Si la función embed_url no puede generar un ID válido, rechazamos la URL.
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
    
# models.py - En la clase Etapa (Refinamiento en youtu.be)
    def embed_url(self):
        """Genera URL embed para YouTube - Versión corregida"""
        if not self.video:
            return ""
    
        try:
            video_id = ""
            
            # 1. Manejar formato youtu.be/l5aj2a8x2qs
            if 'youtu.be/' in self.video:
                # Extraer ID: Quita youtu.be/, luego quita cualquier parámetro de consulta (ej. ?t=)
                video_id = self.video.split('youtu.be/')[1].split('?')[0][:11]
            
            # 2. Manejar formato estándar watch?v=l5aj2a8x2qs
            elif 'watch?v=' in self.video:
                # Extraer ID: Quita watch?v=, luego quita cualquier otro parámetro (ej. &list=)
                video_id = self.video.split('watch?v=')[1].split('&')[0][:11]
                
            # 3. Solo si se obtuvo un ID válido de 11 caracteres
            if len(video_id) == 11:
                # Retornar la URL de embed
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
    icono = models.CharField('Ícono', max_length=50, default='fas fa-question-circle')
    orden = models.IntegerField('Orden', default=1)
    
    class Meta:
        ordering = ['etapa', 'orden']
        verbose_name = 'Tema de Consulta'
        verbose_name_plural = 'Temas de Consulta'
    
    def __str__(self):
        return f"{self.nombre} - {self.etapa.nombre}"


class OpcionTema(models.Model):
    """Opciones para cada tema (respuestas posibles)"""
    tema = models.ForeignKey(TemaConsulta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.TextField('Texto de la opción')
    es_correcta = models.BooleanField('Es correcta', default=False)
    retroalimentacion = models.TextField('Retroalimentación', blank=True)
    lleva_a_etapa = models.ForeignKey(Etapa, on_delete=models.SET_NULL, null=True, blank=True,
                                     help_text="Etapa a la que redirige si se selecciona esta opción")
    
    class Meta:
        verbose_name = 'Opción de Tema'
        verbose_name_plural = 'Opciones de Tema'
    
    def __str__(self):
        return f"{self.texto[:50]}... ({'✓' if self.es_correcta else '✗'})"


class PreguntaEtapa(models.Model):
    Etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='preguntas')
    pregunta = models.TextField('Pregunta')
    
    class Meta:
        verbose_name = 'Pregunta de Etapa'
        verbose_name_plural = 'Preguntas de Etapa'
    
    def __str__(self):
        return f"{self.pregunta[:50]}..."


class RespuestaEtapa(models.Model):
    pregunta = models.ForeignKey(PreguntaEtapa, on_delete=models.CASCADE, related_name='respuestas')
    texto = models.TextField('Texto de respuesta', blank=True)
    correcta = models.BooleanField('Correcta', default=False)
    retroalimentacion = models.TextField('Retroalimentación')
    
    class Meta:
        verbose_name = 'Respuesta de Etapa'
        verbose_name_plural = 'Respuestas de Etapa'
    
    def __str__(self):
        texto_corto = self.texto[:50] if self.texto else self.retroalimentacion[:50]
        return f"{texto_corto}... ({'✓' if self.correcta else '✗'})"
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.contrib.auth.models import User
from .models import *

# -------------------------------
# FORMULARIO PERSONALIZADO DOCENTE
# -------------------------------
class DocenteForm(forms.ModelForm):
    correo = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.TextInput(attrs={'class': 'vTextField', 'size': 32})  # Usar TextInput, no EmailInput
    )

    class Meta:
        model = Docente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa el correo si el User ya existe
        if self.instance and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['correo'].initial = self.instance.user.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Crea User si no existe
        if not hasattr(instance, 'user') or instance.user is None:
            from django.contrib.auth.models import User
            # Se puede crear un usuario temporal con username igual al nombre+apellido
            username = f"{instance.nombre_docente.lower()}.{instance.apellido_docente.lower()}"
            user = User.objects.create(username=username, email=self.cleaned_data['correo'])
            instance.user = user
        else:
            # Actualiza el correo si el User ya existe
            instance.user.email = self.cleaned_data['correo']
            instance.user.save()

        if commit:
            instance.save()
        return instance

# -------------------------------
# ADMIN DOCENTE
# -------------------------------
class DocenteAdmin(admin.ModelAdmin):
    form = DocenteForm

    list_display = (
        'nombre_docente',
        'apellido_docente',
        'obtener_correo',
        'foto_preview',
        'pais_docente',
    )
    search_fields = ('nombre_docente',)
    readonly_fields = ('foto_preview',) 
    fieldsets = (
        (None, {
            'fields': (
                'nombre_docente',
                'apellido_docente',
                'correo',            # Ahora editable
                'pais_docente', 
                'foto_perfil_docente',          
                'foto_preview',   
            )
        }),
    )

    def obtener_correo(self, obj):
        # Protege el acceso a user
        try:
            return obj.user.email
        except (AttributeError, User.DoesNotExist):
            return "No asignado"

    obtener_correo.short_description = 'Correo Electrónico'

    def foto_preview(self, obj): 
        if obj.foto_perfil_docente:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 50%;" />',
                obj.foto_perfil_docente.url
            )
        return "Sin foto"
    foto_preview.short_description = "Foto de perfil"

# -------------------------------
# ADMIN CURSO
# -------------------------------
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_del_Curso',
        'fecha_realización_curso',
    )
    search_fields = ('nombre_del_Curso',)

# -------------------------------
# REGISTER MODELS
# -------------------------------
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Curso, CursoAdmin)

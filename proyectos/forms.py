from django import forms
from .models import Tarea
from .models import Mensaje
from .models import Comentario

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_limite', 'estado', 'usuarios_asignados']
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        # Si el usuario NO es administrador, solo puede modificar la descripción y marcar como completada
        if usuario and not usuario.is_superuser:
            self.fields.pop('titulo')
            self.fields.pop('fecha_limite')
            self.fields.pop('usuarios_asignados')
            self.fields['estado'].choices = [('completada', 'Completada')]  # Solo puede marcar como completada
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        exclude = ['fecha_envio']  # Excluye el campo 'fecha_envio' del formulario
        fields = ['contenido', 'proyecto', 'destinatario', 'remitente', 'fecha_envio']
        widgets = {
            'contenido': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }

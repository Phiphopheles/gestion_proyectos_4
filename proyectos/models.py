from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def get_default_user():
    return User.objects.get(username="default_user").id

class Proyecto(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    usuarios_asignados = models.ManyToManyField(User, through="GrupoProyecto", related_name="proyectos")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
        return self.nombre
    
# Modelo de Tarea
class Tarea(models.Model):
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, related_name="tareas")
    nombre = models.CharField(max_length=100, default='Sin nombre')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    completada = models.BooleanField(default=False)
    titulo = models.CharField(max_length=200)
    usuarios_asignados = models.ManyToManyField(User, related_name="tareas")
    estado = models.CharField(max_length=50, choices=[("pendiente", "Pendiente"), ("completado", "Completado")])
    fecha_limite = models.DateField()
    descripcion = models.TextField()
    nueva_columna_temporal = models.CharField(max_length=50, null=True, blank=True)

    
    def __str__(self):
        return f"{self.titulo} ({self.nombre}) ({self.get_estado_display()})"
    
 

# Modelo de Mensaje
class Mensaje(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="mensajes")
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes_enviados")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, default=4)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)  
    fecha_envio = models.DateTimeField(null=True, blank=True)
   

    def __str__(self):
        return f"Mensaje de {self.remitente} para {self.destinatario} en {self.proyecto}"
        return f"De {self.emisor.username} para {self.receptor.username if self.receptor else 'Proyecto'}"

    
class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor} en {self.tarea}"

class GrupoProyecto(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('miembro', 'Miembro'),
        ('invitado', 'Invitado'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='invitado')

    class Meta:
        unique_together = ('proyecto', 'usuario')

    def __str__(self):
        return f'{self.usuario.username} - {self.proyecto.titulo} - {self.get_rol_display()}'

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.mensaje}"
        return f"Notificación para {self.usuario.username} - {'Leída' if self.leida else 'No leída'}"


# Modelo de Grupo
class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    miembros = models.ManyToManyField(User, related_name="grupos_donde_soy_miembro")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="grupos")
    usuarios = models.ManyToManyField(User, related_name="grupos_donde_soy_usuario")
    ROLES = (
        ("admin", "Administrador"),
        ("miembro", "Miembro"),
        ("invitado", "Invitado"),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default="miembro")


    def __str__(self):  
        return f"{self.nombre} ({self.proyecto.nombre})"  
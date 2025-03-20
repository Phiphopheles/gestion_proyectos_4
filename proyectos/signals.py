from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notificacion, Tarea, Mensaje, Comentario

# Notificación cuando se asigna una nueva tarea
@receiver(post_save, sender=Tarea)
def notificar_tarea_asignada(sender, instance, created, **kwargs):
    if created:
        for usuario in instance.usuarios_asignados.all():
            Notificacion.objects.create(
                usuario=usuario,
                mensaje=f"Se te ha asignado una nueva tarea: {instance.titulo}"
            )

# Notificación cuando se recibe un nuevo mensaje en un proyecto
@receiver(post_save, sender=Mensaje)
def notificar_nuevo_mensaje(sender, instance, created, **kwargs):
    if created:
        for usuario in instance.proyecto.usuarios_asignados.all():
            if usuario != instance.remitente:
                Notificacion.objects.create(
                    usuario=usuario,
                    mensaje=f"Nuevo mensaje en el proyecto {instance.proyecto.titulo} de {instance.remitente.username}"
                )

# Notificación cuando alguien comenta en una tarea
@receiver(post_save, sender=Comentario)
def notificar_nuevo_comentario(sender, instance, created, **kwargs):
    if created:
        for usuario in instance.tarea.usuarios_asignados.all():
            if usuario != instance.autor:
                Notificacion.objects.create(
                    usuario=usuario,
                    mensaje=f"Nuevo comentario en la tarea {instance.tarea.titulo}"
                )

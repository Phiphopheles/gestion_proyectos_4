from django.contrib import admin
from .models import Proyecto, Tarea, Mensaje, Comentario, GrupoProyecto, Notificacion, Grupo

admin.site.register(Proyecto)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha_creacion", "completada")

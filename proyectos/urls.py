from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Página de login usando la vista genérica
    path('signup/', views.signup, name='signup'),  # Página de registro
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('mensaje/<int:proyecto_id>/', views.enviar_mensaje, name='enviar_mensaje_proyecto'),
    path('mensaje_usuario/<int:usuario_id>/', views.enviar_mensaje, name='enviar_mensaje_usuario'),
    path('comentario/<int:tarea_id>/', views.agregar_comentario, name='agregar_comentario'),
    path('proyecto/<int:proyecto_id>/gestionar_grupos/', views.gestionar_grupos, name='gestionar_grupos'),
    path('notificaciones/', views.ver_notificaciones, name='ver_notificaciones'),
]

from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'gestion_proyectos_3'  # Nombre correcto de la app

urlpatterns = [
    path('', views.proyectos_list, name='proyectos_list'),  # Página principal con la lista de proyectos
    path('signup/', views.signup, name='signup'),  # Registro de usuarios
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('mensaje/<int:proyecto_id>/', views.enviar_mensaje, name='enviar_mensaje_proyecto'),
    path('mensaje_usuario/<int:usuario_id>/', views.enviar_mensaje, name='enviar_mensaje_usuario'),
    path('comentario/<int:tarea_id>/', views.agregar_comentario, name='agregar_comentario'),
    path('proyecto/<int:proyecto_id>/gestionar_grupos/', views.gestionar_grupos, name='gestionar_grupos'),
    path('notificaciones/', views.ver_notificaciones, name='ver_notificaciones'),
    path('proyecto/<int:proyecto_id>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyecto/nuevo/', views.proyecto_create, name='proyecto_create'),
    path('proyecto/<int:proyecto_id>/tarea/nueva/', views.tarea_create, name='tarea_create'),
    path('proyecto/<int:proyecto_id>/grupo/nuevo/', views.grupo_create, name='grupo_create'),
    path('login/', LoginView.as_view(template_name='registration/login.html', next_page='gestion_proyectos_3:proyectos_list'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('proyectos.urls')),  # Incluir rutas de la app proyectos
]

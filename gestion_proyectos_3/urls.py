from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel de administración de Django
    path('', include('proyectos.urls')),  # Incluir rutas de la app "proyectos"
    path('accounts/', include('django.contrib.auth.urls')),  # Esto gestiona las rutas de login/logout
    path('proyectos/', include('proyectos.urls')),  # Redirige las URLs que comienzan con 'proyectos/' a proyectos/urls.py
]
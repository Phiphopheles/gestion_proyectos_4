from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import TareaForm, ComentarioForm, ProyectoForm, GrupoForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import MensajeForm
from .models import Proyecto, GrupoProyecto, Tarea, Grupo
from django.http import HttpResponseForbidden
from .models import Notificacion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

@login_required
def enviar_mensaje(request, proyecto_id=None, usuario_id=None):
    proyecto = None
    destinatario = None

    if proyecto_id:
        proyecto = Proyecto.objects.get(id=proyecto_id)
    if usuario_id:
        destinatario = User.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.proyecto = proyecto
            mensaje.destinatario = destinatario
            mensaje.save()
            return redirect('gestion_proyectos_3:proyecto_detail', proyecto.id)
    else:
        form = MensajeForm()

    return render(request, 'proyectos/enviar_mensaje.html', {'form': form, 'proyecto': proyecto, 'destinatario': destinatario})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Solo los usuarios asignados o administradores pueden editar
    if request.user not in tarea.usuarios_asignados.all() and not request.user.is_superuser:
        return redirect('gestion_proyectos_3:lista_tareas')

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea, usuario=request.user)
        if form.is_valid():
            form.save()
            return redirect('gestion_proyectos_3:lista_tareas')
    else:
        form = TareaForm(instance=tarea, usuario=request.user)

@login_required
def lista_tareas(request):
    tareas = Tarea.objects.all().order_by('fecha_limite')  # Ordenadas por fecha límite

    # Obtener parámetros de filtrado desde la URL
    estado = request.GET.get('estado')
    usuario_id = request.GET.get('usuario')
    proyecto_id = request.GET.get('proyecto')

    if estado:
        tareas = tareas.filter(estado=estado)
    if usuario_id:
        tareas = tareas.filter(usuarios_asignados__id=usuario_id)
    if proyecto_id:
        tareas = tareas.filter(proyecto__id=proyecto_id)

    usuarios = User.objects.all()
    proyectos = Proyecto.objects.all()

    return render(request, 'proyectos/lista_tareas.html', {
        'tareas': tareas,
        'usuarios': usuarios,
        'proyectos': proyectos,
    })

@login_required
def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False).order_by('-fecha_creacion')
    return render(request, 'proyectos/notificaciones.html', {'notificaciones': notificaciones})

@login_required
def agregar_comentario(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarea = tarea
            comentario.save()
            return redirect('gestion_proyectos_3:lista_tareas')
    else:
        form = ComentarioForm()

    return render(request, 'proyectos/agregar_comentario.html', {'form': form, 'tarea': tarea})

@login_required
def gestionar_grupos(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Solo los administradores pueden gestionar los grupos
    if not GrupoProyecto.objects.filter(proyecto=proyecto, usuario=request.user, rol='admin').exists():
        return HttpResponseForbidden("No tienes permisos para gestionar los grupos de este proyecto.")

    usuarios = User.objects.all()
    grupos = GrupoProyecto.objects.filter(proyecto=proyecto)
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        rol = request.POST.get('rol')
        
        usuario = get_object_or_404(User, id=usuario_id)
        # Crear o actualizar la asignación de grupo con rol
        grupo_proyecto, created = GrupoProyecto.objects.update_or_create(
            proyecto=proyecto,
            usuario=usuario,
            defaults={'rol': rol}
        )
        
        return redirect('gestion_proyectos_3:gestionar_grupos', proyecto_id=proyecto.id)

    return render(request, 'proyectos/gestionar_grupos.html', {'proyecto': proyecto, 'usuarios': usuarios, 'grupos': grupos})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_proyectos_3:login')  # Redirige al login después de registrarse
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def proyectos_list(request):
    if request.user.is_superuser:
        proyectos = Proyecto.objects.all()
    else:
        proyectos = Proyecto.objects.filter(grupoproyecto__usuario=request.user)
    return render(request, 'proyectos/proyectos_list.html', {'proyectos': proyectos})

@login_required
@permission_required('proyectos.add_proyecto', raise_exception=True)
def proyecto_create(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_proyectos_3:proyectos_list')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/proyecto_form.html', {'form': form})

@login_required
@permission_required('proyectos.add_tarea', raise_exception=True)
def tarea_create(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if not request.user.groups.filter(name='Administrador').exists():
        return redirect('gestion_proyectos_3:proyectos_list')
        
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            return redirect('gestion_proyectos_3:proyecto_detail', proyecto_id=proyecto.id)
    else:
        form = TareaForm()
    return render(request, 'proyectos/tarea_form.html', {'form': form, 'proyecto': proyecto})

@login_required
def proyecto_detail(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    tareas = Tarea.objects.filter(proyecto=proyecto)
    return render(request, 'proyectos/proyecto_detail.html', {'proyecto': proyecto, 'tareas': tareas})

@login_required
@permission_required('proyectos.add_grupo', raise_exception=True)
def grupo_create(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.proyecto = proyecto
            grupo.save()
            return redirect('gestion_proyectos_3:proyecto_detail', proyecto_id=proyecto.id)
    else:
        form = GrupoForm()
    return render(request, 'proyectos/grupo_form.html', {'form': form, 'proyecto': proyecto})

def logout_view(request):
    logout(request)
    return redirect('gestion_proyectos_3:login')

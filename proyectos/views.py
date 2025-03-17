from django.shortcuts import render, get_object_or_404, redirect
from .models import Tarea, Proyecto
from django.contrib.auth.models import User
from .forms import TareaForm, ComentarioForm
from django.contrib.auth.decorators import login_required
from .forms import MensajeForm
from .models import Proyecto, GrupoProyecto
from django.http import HttpResponseForbidden
from .models import Notificacion
from django.contrib.auth.forms import UserCreationForm


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
            return redirect('detalle_proyecto', proyecto.id)
    else:
        form = MensajeForm()

    return render(request, 'proyectos/enviar_mensaje.html', {'form': form, 'proyecto': proyecto, 'destinatario': destinatario})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Solo los usuarios asignados o administradores pueden editar
    if request.user not in tarea.usuarios_asignados.all() and not request.user.is_superuser:
        return redirect('lista_tareas')

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea, usuario=request.user)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea, usuario=request.user)

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
            return redirect('detalle_tarea', tarea.id)
    else:
        form = ComentarioForm()

    return render(request, 'proyectos/agregar_comentario.html', {'form': form, 'tarea': tarea})

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
        
        return redirect('gestionar_grupos', proyecto_id=proyecto.id)

    return render(request, 'proyectos/gestionar_grupos.html', {'proyecto': proyecto, 'usuarios': usuarios, 'grupos': grupos})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después de registrarse
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Proyecto, Tarea, Comentario,Usuario, User
from django.utils.timezone import now
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        descripcion = request.POST.get('descripcion')
        email = request.POST.get('email')
        activo = request.POST.get('activo') == 'on'  # Si el checkbox "activo" está marcado
        nuevo_usuario = Usuario.objects.create(nombre=nombre,apellido=apellido,descripcion=descripcion,
            email=email,activo=activo)

        messages.success(request, 'Usuario creado con éxito')
        return redirect('listar_usuarios')

    return render(request, 'crear_usuario.html')

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.email = request.POST.get('email')
        usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        usuario.activo = request.POST.get('activo') == 'on'  # Si el checkbox "activo" está marcado
        usuario.save()

        messages.success(request, 'Usuario actualizado con éxito')
        return redirect('listar_usuarios')

    return render(request, 'modificar_usuario.html', {'usuario': usuario})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado con éxito')
    return redirect('listar_usuarios')

# Pantalla de inicio con lista de proyectos
def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'listar_proyectos.html', {'proyectos': proyectos})

# Detalles de un proyecto específico
def detalles_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    tareas = proyecto.tareas.all()  # Obtiene las tareas asociadas

    return render(request, 'detalles_proyecto.html', {
        'proyecto': proyecto,
        'tareas': tareas,
        'progreso': proyecto.progreso(),  # Llamada al método progreso
    })


# Crear un nuevo proyecto
def crear_proyecto(request):
    usuarios = Usuario.objects.filter(activo=True)  # Filtrar usuarios activos
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        encargado_nombre = request.POST.get('encargado_nombre')

        # Buscar al usuario por su nombre y apellido
        encargado = None
        if encargado_nombre:
            nombre, apellido = encargado_nombre.split(' ', 1)  # Dividir nombre y apellido
            encargado = Usuario.objects.filter(nombre=nombre, apellido=apellido).first()

        Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            encargado=encargado
        )
        return redirect('listar_proyectos')

    return render(request, 'crear_proyecto.html', {'usuarios': usuarios})

# Editar un proyecto existente
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    usuarios = Usuario.objects.filter(activo=True)  # Solo usuarios activos
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        encargado_nombre = request.POST.get('encargado_nombre')

        # Buscar al usuario por nombre y apellido
        encargado = None
        if encargado_nombre:
            nombre_encargado, apellido_encargado = encargado_nombre.split(' ', 1)
            encargado = Usuario.objects.filter(nombre=nombre_encargado, apellido=apellido_encargado).first()

        proyecto.nombre = nombre
        proyecto.descripcion = descripcion
        proyecto.fecha_inicio = fecha_inicio
        proyecto.fecha_fin = fecha_fin
        proyecto.encargado = encargado
        proyecto.save()

        return redirect('listar_proyectos')
    
    return render(request, 'editar_proyecto.html', {'proyecto': proyecto, 'usuarios': usuarios})
# Eliminar un proyecto
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    return redirect('lista_proyectos')

# Crear una nueva tarea dentro de un proyecto
def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        nombre = request.POST['nombre']  # 'titulo' es el nombre del campo en el formulario, pero se guarda como 'nombre' en el modelo
        descripcion = request.POST['descripcion']
        fecha_limite = request.POST['fecha_limite']
        Tarea.objects.create(  
            proyecto=proyecto,
            nombre=nombre,  # Asegúrate de que este campo se llame 'nombre'
            descripcion=descripcion,
            fecha_limite=fecha_limite
        )
        return redirect('detalles_proyecto', proyecto_id=proyecto.id)
    return render(request, 'crear_tarea.html', {'proyecto': proyecto})

# Actualizar el estado de una tarea
def actualizar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        tarea.completada = request.POST.get('completada') == 'on'
        tarea.save()
        return redirect('detalles_proyecto', proyecto_id=tarea.proyecto.id)
    return render(request, 'actualizar_tarea.html', {'tarea': tarea})

# Agregar un comentario a una tarea
def agregar_comentario(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        contenido = request.POST['contenido']
        Comentario.objects.create(
            tarea=tarea,
            contenido=contenido,
            fecha_creacion=now()
        )
        return redirect('detalles_proyecto', proyecto_id=tarea.proyecto.id)
    return render(request, 'agregar_comentario.html', {'tarea': tarea})

def grafico_proyecto(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'grafico_proyecto.html', {'proyectos': proyectos})

def datos_grafico(request):
    proyectos = Proyecto.objects.all()
    nombres = [proyecto.nombre for proyecto in proyectos]  # Solo los nombres de los proyectos
    duraciones = [(proyecto.fecha_fin - proyecto.fecha_inicio).days for proyecto in proyectos]

    data = {
        "labels": nombres,
        "datasets": [
            {
                "label": "Duración del Proyecto (días)",
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
                "data": duraciones,
            }
        ],
    }
    return JsonResponse(data)

def asignar_encargado(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    usuarios = Usuario.objects.all()  # Obtenemos todos los usuarios disponibles.

    if request.method == 'POST':
        encargado_nombre = request.POST.get('encargado')  # Obtén el nombre enviado.
        if encargado_nombre:
            try:
                encargado = Usuario.objects.get(nombre=encargado_nombre)
                proyecto.encargado = encargado  # Asigna el usuario al proyecto.
                proyecto.save()
                return redirect('detalles_proyecto', proyecto_id=proyecto.id)
            except Usuario.DoesNotExist:
                # Manejar si no se encuentra un usuario con ese nombre.
                return render(request, 'asignar_encargado.html', {
                    'proyecto': proyecto,
                    'usuarios': usuarios,
                    'error': 'El usuario seleccionado no existe.'
                })

    return render(request, 'asignar_encargado.html', {
        'proyecto': proyecto,
        'usuarios': usuarios
    })
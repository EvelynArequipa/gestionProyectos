from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Pantalla de inicio
    path('proyectos/', views.listar_proyectos, name='listar_proyectos'),
    
    #usuario
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Proyecto
    
    path('proyecto/<int:proyecto_id>/', views.detalles_proyecto, name='detalles_proyecto'),
    path('proyecto/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyecto/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('proyecto/<int:proyecto_id>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),

    # Tareas
    path('proyecto/<int:proyecto_id>/tarea/crear/', views.crear_tarea, name='crear_tarea'),
    path('tarea/<int:tarea_id>/actualizar/', views.actualizar_tarea, name='actualizar_tarea'),

    # Comentarios
    path('tarea/<int:tarea_id>/comentario/agregar/', views.agregar_comentario, name='agregar_comentario'),
    
    path('grafico_proyecto/', views.grafico_proyecto, name='grafico_proyecto'),
    path('datos_grafico/', views.datos_grafico, name='datos_grafico'),
    
    

]

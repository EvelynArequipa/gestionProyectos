# Generated by Django 4.0.6 on 2025-01-03 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EquiposDeTrabajo', '0003_remove_proyecto_usuario_alter_proyecto_nombre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarea',
            old_name='nombre',
            new_name='titulo',
        ),
    ]

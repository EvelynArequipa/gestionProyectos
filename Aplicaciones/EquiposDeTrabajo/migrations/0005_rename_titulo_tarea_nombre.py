# Generated by Django 4.0.6 on 2025-01-03 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EquiposDeTrabajo', '0004_rename_nombre_tarea_titulo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarea',
            old_name='titulo',
            new_name='nombre',
        ),
    ]

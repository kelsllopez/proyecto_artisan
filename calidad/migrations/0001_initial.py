# Generated by Django 5.1.1 on 2024-09-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquipoUtensilioLimpieza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Equipo - Utensilio',
                'verbose_name_plural': 'Equipo - Utensilio',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='GrupoEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='GrupoEquipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre del grupo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Grupo Equipos',
                'permissions': (('grupos.listar', 'Puede listar los grupos'), ('grupos.crear', 'Puede crear un grupo'), ('grupos.eliminar', 'Puede eliminar un grupo'), ('grupos.actualizar', 'Puede actualizar un utensilio'), ('grupos.asociar', 'Puede asociar un equipo al utensilio')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='GrupoUtensilio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='RegistroLimpiezaEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observación')),
                ('estado', models.TextField(choices=[('Ejecutado', 'Ejecutado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')], default='Ejecutado', max_length=50)),
                ('accion_correctiva', models.TextField(blank=True, db_column='observacion_correctiva', null=True, verbose_name='Acción Correctiva')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Registro Limpieza Equipo',
                'verbose_name_plural': 'Registro Limpieza Equipos',
                'permissions': (('registrolimpiezaequipo.listar', 'Puede ver los registros'), ('registrolimpiezaequipo.administrador', 'Puede ver todos los registros'), ('registrolimpiezaequipo.crear', 'Puede añadir un registro'), ('registrolimpiezaequipo.eliminar', 'Puede eliminar un registro'), ('registrolimpiezaequipo.actualizar', 'Puede actualizar un registro'), ('registrolimpiezaequipo.excel', 'Puede generar un excel')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='RegistroLimpiezaEquipoHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observación')),
                ('estado', models.TextField(choices=[('Ejecutado', 'Ejecutado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')], default='Ejecutado', max_length=50)),
                ('accion_correctiva', models.TextField(blank=True, db_column='observacion_correctiva', null=True, verbose_name='Acción Correctiva')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name': 'Historial Registro Limpiez Equipo',
                'verbose_name_plural': 'Historial Registro Limpieza Equipos',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UtensilioLimpieza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre Artículo')),
                ('categoria', models.CharField(choices=[('utensilio de limpieza', 'Utensilio de Limpieza'), ('detergente', 'Detergente')], max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'utensilio',
                'verbose_name_plural': 'utensilio',
                'permissions': (('utensiliolimpieza.listar', 'Puede ver los utensilios'), ('utensiliolimpieza.crear', 'Puede añadir un utensilio'), ('utensiliolimpieza.eliminar', 'Puede eliminar un utensilio'), ('utensiliolimpieza.actualizar', 'Puede actualizar un utensilio'), ('utensiliolimpieza.asociar', 'Puede asociar un equipo al utensilio')),
                'default_permissions': (),
            },
        ),
    ]
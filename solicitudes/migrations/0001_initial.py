# Generated by Django 5.1.1 on 2024-09-20 15:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0002_initial'),
        ('nucleo', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('No Completada', 'No Completada'), ('Completada', 'Completada')], default='No Completada', max_length=120, verbose_name='Estado solicitud')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('lugar_o', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.bodega', verbose_name='Lugar de Origen')),
                ('solicitante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Persona que solicita')),
            ],
            options={
                'verbose_name': 'solicitud',
                'verbose_name_plural': 'solicitudes',
                'ordering': ['-created'],
                'permissions': (('listar', 'Puede listar las solicitudes'), ('crear', 'Puede crear una solicitud'), ('eliminar', 'Permite eliminar una solicitud'), ('actualizar', 'Permite actualizar una solicitud'), ('detalle', 'Permite ver el detalle de la solicitud')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SolicitudInsumos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(verbose_name='Cantidad a solicitar')),
                ('comentario', models.CharField(default='', max_length=255, verbose_name='Comentario')),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.insumo', verbose_name='Insumo a solicitar')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitud', verbose_name='Solicitud')),
            ],
            options={
                'verbose_name': 'solicitud insumo',
                'verbose_name_plural': 'solicitud insumos',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SolicitudEncargados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Persona que sera notificada')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitud', verbose_name='Solicitud')),
            ],
            options={
                'verbose_name': 'solicitud encargado',
                'verbose_name_plural': 'solicitud encargado',
                'default_permissions': (),
                'unique_together': {('solicitud', 'encargado')},
            },
        ),
    ]
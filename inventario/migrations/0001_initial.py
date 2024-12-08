# Generated by Django 5.1.1 on 2024-09-20 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Ubicación de la bodega')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'bodega',
                'verbose_name_plural': 'bodegas',
                'ordering': ['-id'],
                'permissions': (('bodega.listar', 'Puede ver el listado de las bodegas'), ('bodega.crear', 'Puede crear una bodega'), ('bodega.eliminar', 'Permite eliminar una bodega'), ('bodega.actualizar', 'Permite actualizar una bodega'), ('bodega.valorizar', 'Permite valorizar la bodega')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistorialBodegaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.BigIntegerField(verbose_name='Cantidad')),
                ('precio', models.FloatField(verbose_name='Precio del producto a la fecha')),
            ],
            options={
                'verbose_name': 'historial bodega producto',
                'verbose_name_plural': 'historial bodega productos',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='InsumoBulto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lotep', models.CharField(blank=True, default='', max_length=255, verbose_name='Lote Proveedor')),
                ('cantidad', models.FloatField(verbose_name='Cantidad de unidades en el bulto')),
                ('cantidadu', models.FloatField(default=0, verbose_name='Cantidad de unidades utilizadas')),
                ('formato', models.FloatField(default=0, verbose_name='Formato')),
                ('formatoo', models.FloatField(default=1, verbose_name='Formato Original')),
                ('numero', models.IntegerField(verbose_name='Número bulto')),
            ],
        ),
        migrations.CreateModel(
            name='InsumoBultoHijo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Insumo Bulto Hijo',
                'verbose_name_plural': 'Insumo Bulto Hijos',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='InventarioInsumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(default='Bien', max_length=20, verbose_name='Estado')),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'inventario Insumo',
                'verbose_name_plural': 'inventario Insumos',
                'ordering': ['insumo__nombre'],
                'permissions': (('inventarioi.listar', 'Puede ver el listado de los insumos'), ('inventarioi.global', 'Puede ver el listado de los insumos globales'), ('inventarioi.actualizar', 'Permite actualizar un insumo')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='InventarioProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.BigIntegerField(verbose_name='Cantidad')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'inventario Producto',
                'verbose_name_plural': 'inventario Productos',
                'ordering': ['producto__nombre'],
                'permissions': (('inventariop.listar', 'Puede ver el listado de los productos'), ('inventariop.actualizar', 'Permite actualizar un producto'), ('inventariop.global', 'Permite el listado de los productos globales')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SupervisorBodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'supervisor bodega',
                'verbose_name_plural': 'supervisor bodegas',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistorialBodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manual', models.BooleanField(default=False, verbose_name='Historial Manual')),
                ('fecha', models.DateTimeField(verbose_name='Fecha de Historial')),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.bodega', verbose_name='Bodega')),
            ],
            options={
                'verbose_name': 'historial bodega',
                'verbose_name_plural': 'historial bodegas',
                'ordering': ['-id'],
                'permissions': (('historial.listar', 'Puede ver el listado de los historiales de bodega'), ('historial.crear', 'Puede crear un historial de bodega')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistorialBodegaInsumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.BigIntegerField(verbose_name='Cantidad')),
                ('precio', models.FloatField(verbose_name='Precio del insumo a la fecha')),
                ('historialbodega', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.historialbodega', verbose_name='Bodega')),
            ],
            options={
                'verbose_name': 'historial insumo',
                'verbose_name_plural': 'historial insumo',
                'ordering': ['insumo__nombre'],
                'default_permissions': (),
            },
        ),
    ]

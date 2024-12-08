# Generated by Django 5.1.1 on 2024-10-24 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventarioinsumo',
            options={'default_permissions': (), 'ordering': ['insumo__nombre'], 'permissions': (('inventarioi.listar', 'Puede ver el listado de los insumos'), ('inventarioi.global', 'Puede ver el listado de los insumos globales'), ('inventarioi.actualizar', 'Permite actualizar un insumo')), 'verbose_name': 'Inventario Insumo', 'verbose_name_plural': 'Inventarios Insumos'},
        ),
        migrations.AlterField(
            model_name='inventarioinsumo',
            name='bodega',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.bodega', verbose_name='Bodega'),
        ),
    ]

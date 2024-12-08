# Generated by Django 5.1.1 on 2024-10-24 15:34

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0007_alter_linea_options_and_more'),
        ('proveedores', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='insumoelaboracionproducto',
            options={'default_permissions': (), 'ordering': ['insumo__nombre'], 'verbose_name': 'Insumo para Producto', 'verbose_name_plural': 'Insumos para Productos'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'default_permissions': (), 'ordering': ['id'], 'permissions': (('producto.listar', 'Puede ver los productos'), ('producto.crear', 'Puede crear un producto'), ('producto.eliminar', 'Puede eliminar un producto'), ('producto.actualizar', 'Puede actualizar un producto')), 'verbose_name': 'producto', 'verbose_name_plural': 'productos'},
        ),
        migrations.AddField(
            model_name='insumodirectoproducto',
            name='precio_proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proveedores.proveedorinsumo', verbose_name='Precio del proveedor'),
        ),
        migrations.AddField(
            model_name='insumoelaboracionproducto',
            name='precio_provedor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insumo_elaboracion_producto_precios', to='proveedores.proveedorinsumo', verbose_name='Precio de proveedor'),
        ),
        migrations.AlterField(
            model_name='insumodirectoproducto',
            name='cantidad',
            field=models.IntegerField(verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='insumoelaboracionproducto',
            name='cantidad',
            field=models.FloatField(help_text='Cantidad de insumo necesario por kilo del producto.', validators=[django.core.validators.MinValueValidator(0.1)], verbose_name='Cantidad por kilo'),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='fecha',
            field=models.CharField(max_length=255, verbose_name='Fecha de extracción'),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='nombre',
            field=models.CharField(max_length=255, verbose_name='Nombre Moneda'),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor Moneda'),
        ),
        migrations.AlterField(
            model_name='rama',
            name='nombre',
            field=models.CharField(max_length=255, verbose_name='Nombre del área de negocio'),
        ),
    ]

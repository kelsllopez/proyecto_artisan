# Generated by Django 5.1.1 on 2024-11-01 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0002_alter_proveedor_empresa_rut_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='empresa_rut',
            field=models.CharField(max_length=50, unique=True, verbose_name='Rut Empresa'),
        ),
        migrations.AlterField(
            model_name='proveedorinsumo',
            name='precio',
            field=models.FloatField(verbose_name='Precio'),
        ),
    ]
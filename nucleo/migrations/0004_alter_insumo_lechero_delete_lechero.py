# Generated by Django 5.1.1 on 2024-10-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0003_lechero_insumo_lechero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='lechero',
            field=models.CharField(default='Desconocido', max_length=100, verbose_name='Nombre del lechero'),
        ),
        migrations.DeleteModel(
            name='Lechero',
        ),
    ]
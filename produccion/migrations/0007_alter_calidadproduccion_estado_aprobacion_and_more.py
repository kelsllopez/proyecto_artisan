# Generated by Django 5.1.1 on 2024-11-11 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0006_calidadproduccion_estado_aprobacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calidadproduccion',
            name='estado_aprobacion',
            field=models.TextField(choices=[('Desaprobado', 'Desaprobado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')], default='Pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalcalidadproduccion',
            name='estado_aprobacion',
            field=models.TextField(choices=[('Desaprobado', 'Desaprobado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')], default='Pendiente', max_length=50),
        ),
    ]

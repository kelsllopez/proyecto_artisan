# Generated by Django 5.1.1 on 2024-10-05 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0004_alter_insumo_lechero_delete_lechero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insumo',
            name='lechero',
        ),
    ]
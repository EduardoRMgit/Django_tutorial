# Generated by Django 2.2.8 on 2020-05-20 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0011_auto_20200518_2218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comision',
            options={'verbose_name_plural': 'Comisiones'},
        ),
        migrations.AlterModelOptions(
            name='errorestransaccion',
            options={'verbose_name_plural': 'Errores de Transacción'},
        ),
        migrations.AlterModelOptions(
            name='tipotransaccion',
            options={'verbose_name_plural': 'Tipos de Transaccion'},
        ),
    ]

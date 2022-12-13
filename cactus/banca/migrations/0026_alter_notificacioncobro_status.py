# Generated by Django 3.2 on 2022-12-13 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0025_notificacioncobro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacioncobro',
            name='status',
            field=models.CharField(choices=[('P', 'Pendiente'), ('L', 'Liquidado'), ('D', 'Declinado'), ('V', 'Vencido')], default='P', max_length=32),
        ),
    ]

# Generated by Django 3.2 on 2022-12-16 03:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0057_contacto_bloqueado'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 3.2 on 2022-12-08 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0056_contacto_es_inguz'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='bloqueado',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

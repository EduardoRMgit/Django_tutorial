# Generated by Django 3.2 on 2023-05-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0080_userprofile_contador_servicio_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pep',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.2.8 on 2021-02-18 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0041_auto_20210217_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docextraction',
            name='user',
        ),
    ]

# Generated by Django 3.2 on 2023-02-09 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0071_delete_respaldo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='comprobanteDomCaptura',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='ineCaptura',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='ineReversoCaptura',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='saldo_dde',
        ),
    ]

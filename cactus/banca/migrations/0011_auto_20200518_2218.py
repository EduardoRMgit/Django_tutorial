# Generated by Django 2.2.8 on 2020-05-19 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0010_mediosdisponibles'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TransaccionCancelada',
        ),
        migrations.DeleteModel(
            name='TransaccionExterna',
        ),
    ]

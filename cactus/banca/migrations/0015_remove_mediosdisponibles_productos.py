# Generated by Django 2.2.8 on 2020-09-18 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0014_auto_20200714_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediosdisponibles',
            name='productos',
        ),
    ]

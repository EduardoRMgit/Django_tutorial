# Generated by Django 3.2 on 2023-03-15 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0074_alter_docadjunto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='docadjunto',
            name='imagen_url',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
    ]
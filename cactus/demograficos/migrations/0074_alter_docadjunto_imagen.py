# Generated by Django 3.2 on 2023-03-15 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0073_alter_docadjunto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docadjunto',
            name='imagen',
            field=models.ImageField(blank=True, max_length=2048, null=True, upload_to=''),
        ),
    ]
# Generated by Django 3.2 on 2023-06-30 08:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spei', '0025_stptransaction_url_cep'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentapersonafisica',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 3.2 on 2023-02-07 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pld', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='riesgo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.2 on 2023-06-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0038_auto_20230623_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamozakitransaccion',
            name='monto_total',
            field=models.CharField(max_length=64, null=True),
        ),
    ]

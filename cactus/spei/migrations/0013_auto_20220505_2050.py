# Generated by Django 2.2.8 on 2022-05-06 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spei', '0012_stpnotificacionestadodecuenta'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolioStp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.IntegerField(default=100)),
            ],
        ),
        migrations.AddField(
            model_name='cuentapersonafisica',
            name='folio_stp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2 on 2023-05-02 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0034_merge_20230303_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comisionestp',
            name='transaccion',
        ),
        migrations.AddField(
            model_name='comisionestp',
            name='rangotransacciones',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transaccion',
            name='comision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='banca.comisionestp'),
        ),
    ]
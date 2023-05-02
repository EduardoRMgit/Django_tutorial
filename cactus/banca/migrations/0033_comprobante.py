# Generated by Django 3.2 on 2023-02-15 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0032_alter_transaccion_monto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(unique=True)),
                ('template', models.ImageField(upload_to='docs/plantillas')),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='banca.tipotransaccion')),
            ],
            options={
                'verbose_name': 'Template de Comprobante',
                'verbose_name_plural': 'Templates de Comprobantes',
            },
        ),
    ]

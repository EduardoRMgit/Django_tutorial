# Generated by Django 2.2.8 on 2020-08-04 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_servicio', models.IntegerField(blank=True, null=True)),
                ('Imagenes_referencia', models.ImageField(blank=True, null=True, upload_to='servicios/referencia/')),
            ],
            options={
                'verbose_name_plural': 'Imagenes de Referencia',
            },
        ),
        migrations.CreateModel(
            name='Logotypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_servicio', models.IntegerField(blank=True, null=True)),
                ('Logo', models.ImageField(blank=True, null=True, upload_to='servicios/logos/')),
            ],
            options={
                'verbose_name_plural': 'Logotipos',
            },
        ),
        migrations.CreateModel(
            name='TransactionGpo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('Servicio', models.CharField(max_length=69)),
                ('Producto', models.CharField(max_length=69)),
                ('Precio', models.CharField(max_length=69)),
                ('Resp', models.CharField(blank=True, max_length=100, null=True)),
                ('Comision_GPO', models.CharField(blank=True, max_length=69, null=True)),
                ('Comision_BratD', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('Saldo_Cliente', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=14, null=True)),
                ('ID_TX', models.CharField(blank=True, max_length=100, null=True)),
                ('Num_Aut', models.CharField(blank=True, max_length=100, null=True)),
                ('codigo', models.CharField(blank=True, max_length=100, null=True)),
                ('Referencia', models.CharField(blank=True, max_length=100, null=True)),
                ('Err', models.CharField(blank=True, max_length=100, null=True)),
                ('stat_code', models.CharField(blank=True, max_length=100, null=True)),
                ('Telefono', models.CharField(blank=True, max_length=25, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transacciones',
            },
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Servicio', models.CharField(blank=True, max_length=100, null=True)),
                ('Producto', models.CharField(blank=True, max_length=100, null=True)),
                ('id_servicio', models.IntegerField(blank=True, null=True)),
                ('id_producto', models.IntegerField(blank=True, null=True)),
                ('id_CatTipoServicio', models.IntegerField(blank=True, null=True)),
                ('Tipo_Front', models.CharField(blank=True, max_length=100, null=True)),
                ('hasDigitToVerificator', models.BooleanField(blank=True, default=False, null=True)),
                ('Precio', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('ShowAyuda', models.BooleanField(blank=True, default=True, null=True)),
                ('Comision_GPO', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('Comision_BratD', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('Comision', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('Tipo_Referencia', models.CharField(blank=True, max_length=10, null=True)),
                ('imgref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios.ImgRef')),
                ('logotypes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios.Logotypes')),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
    ]

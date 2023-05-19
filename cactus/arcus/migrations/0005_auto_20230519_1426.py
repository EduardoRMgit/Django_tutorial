# Generated by Django 3.2 on 2023-05-19 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banca', '0036_alter_comisionestp_rangotransacciones'),
        ('arcus', '0004_auto_20230515_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagosArcus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_transaccion', models.CharField(blank=True, max_length=2056, null=True)),
                ('tipo', models.CharField(blank=True, max_length=256, null=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('moneda', models.CharField(blank=True, max_length=20, null=True)),
                ('identificador', models.CharField(blank=True, max_length=256, null=True)),
                ('comision', models.FloatField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
                ('estatus', models.CharField(blank=True, max_length=2056, null=True)),
                ('id_externo', models.CharField(blank=True, max_length=2056, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=2056, null=True)),
                ('numero_cuenta', models.CharField(blank=True, max_length=12, null=True)),
                ('empresa_recargas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arcus.recargasarcus')),
                ('empresa_servicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arcus.servicesarcus')),
                ('transaccion', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaccion_arcus', to='banca.transaccion')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pagos arcus',
            },
        ),
        migrations.DeleteModel(
            name='TiempoAire',
        ),
    ]

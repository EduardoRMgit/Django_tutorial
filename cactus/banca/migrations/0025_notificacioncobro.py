# Generated by Django 3.2 on 2022-12-09 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banca', '0024_auto_20221207_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificacionCobro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_contacto_solicitante', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('importe', models.DecimalField(blank=True, decimal_places=4, max_digits=30, null=True)),
                ('status', models.CharField(choices=[('P', 'Pendiente'), ('L', 'Liquidado'), ('D', 'Declinado')], default='P', max_length=32)),
                ('concepto', models.CharField(blank=True, max_length=512, null=True)),
                ('referencia_numerica', models.CharField(max_length=64, null=True)),
                ('clave_rastreo', models.CharField(max_length=64, null=True)),
                ('transaccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cobros', to='banca.inguztransaction')),
                ('usuario_deudor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mis_notificaciones_cobro', to=settings.AUTH_USER_MODEL)),
                ('usuario_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cobros_solicitados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cobros',
            },
        ),
    ]
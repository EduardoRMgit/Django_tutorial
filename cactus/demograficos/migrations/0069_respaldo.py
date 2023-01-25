# Generated by Django 3.2.16 on 2023-01-24 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demograficos', '0068_userprofile_pais_origen_otro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Respaldo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'APROBADA'), ('P', 'PENDIENTE'), ('D', 'DECLINADA')], default='P', max_length=10, verbose_name='Solicitud')),
                ('contacto_id', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='ID del contacto')),
                ('contrato_ordenante', models.FileField(blank=True, null=True, upload_to='contratos-respaldos')),
                ('contrato_respaldo', models.FileField(blank=True, null=True, upload_to='contratos-respaldos')),
                ('activo', models.BooleanField(default=True)),
                ('ordenante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respaldos', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('respaldo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respaldados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Respaldos',
            },
        ),
    ]

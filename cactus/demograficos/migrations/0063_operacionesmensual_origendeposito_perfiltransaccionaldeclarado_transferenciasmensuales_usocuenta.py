# Generated by Django 3.2 on 2023-01-11 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demograficos', '0062_direccion_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperacionesMensual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operaciones_mensuales', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrigenDeposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransferenciasMensuales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transferencias_mensuales', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsoCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uso_de_cuenta', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilTransaccionalDeclarado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_perfil', models.CharField(blank=True, choices=[('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')], max_length=50, null=True)),
                ('operaciones_mensuales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demograficos.operacionesmensual')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demograficos.origendeposito')),
                ('transferencias_mensuales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demograficos.transferenciasmensuales')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_perfil', to=settings.AUTH_USER_MODEL)),
                ('uso_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demograficos.usocuenta')),
            ],
        ),
    ]

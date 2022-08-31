# Generated by Django 2.2.8 on 2020-05-07 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banca', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fondeador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apMaterno', models.CharField(max_length=50)),
                ('RFC', models.CharField(max_length=15)),
                ('limiteMaximoDeFondeo', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fondeador', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PagoFondeador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField()),
                ('fechaCreacion', models.DateTimeField(null=True)),
                ('fechaInicialDeFondeo', models.DateTimeField(null=True)),
                ('fechaFinalDeFondeo', models.DateTimeField(null=True)),
                ('generaInteresesDesde', models.BooleanField(default=True)),
                ('fondeador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dde.Fondeador')),
            ],
        ),
        migrations.CreateModel(
            name='Producto_Fondeador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField()),
                ('fechaCreacion', models.DateTimeField(null=True)),
                ('fechaInicialDeFondeo', models.DateTimeField(null=True)),
                ('fechaFinalDeFondeo', models.DateTimeField(null=True)),
                ('generaInteresesDesde', models.BooleanField(default=True)),
                ('pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dde.PagoFondeador')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='banca.Productos')),
            ],
        ),
        migrations.CreateModel(
            name='RetornoFondeador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPago', models.DateTimeField(null=True)),
                ('monto', models.FloatField()),
                ('tasa_porcentajeAnualizado', models.FloatField()),
                ('productoFondeador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dde.Producto_Fondeador')),
                ('tipoAnual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='banca.TipoAnual')),
            ],
        ),
        migrations.AddField(
            model_name='pagofondeador',
            name='productos',
            field=models.ManyToManyField(through='dde.Producto_Fondeador', to='banca.Productos'),
        ),
    ]

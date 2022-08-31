# Generated by Django 2.2.8 on 2022-06-19 04:25

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0020_valorudis'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaldoReservado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_saldo', models.CharField(choices=[('reservado', 'reservado'), ('aplicado', 'aplicado'), ('devuelto', 'devuelto')], default='reservado', max_length=20)),
                ('fecha_reservado', models.DateTimeField(auto_now=True)),
                ('saldo_reservado', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fecha_aplicado_devuelto', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de aplicación/devolución')),
            ],
        ),
    ]

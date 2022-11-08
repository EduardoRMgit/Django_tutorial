# Generated by Django 3.2.15 on 2022-10-19 17:45

from django.conf import settings
import django.core.validators
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
            name='CashoutM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cashout', models.CharField(max_length=100, verbose_name='ID del retiro')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Monto')),
                ('currency', models.CharField(max_length=50, verbose_name='Moneda de cambio')),
            ],
            options={
                'verbose_name_plural': 'Cashout',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(verbose_name='Categoria')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Categoria',
            },
        ),
        migrations.CreateModel(
            name='CreatePay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Monto del retiro')),
            ],
            options={
                'verbose_name_plural': 'Crear Pago',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant', models.CharField(max_length=50, verbose_name='ID Comercio')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre')),
                ('address', models.CharField(max_length=100, verbose_name='Direccion')),
                ('image', models.CharField(max_length=50, verbose_name='Imagen')),
                ('latitude', models.DecimalField(decimal_places=14, max_digits=17, verbose_name='Latitud')),
                ('longitude', models.DecimalField(decimal_places=14, max_digits=17, verbose_name='Longitud')),
                ('phone', models.CharField(max_length=11, verbose_name='Telefono')),
                ('type', models.IntegerField(verbose_name='Tipo')),
            ],
            options={
                'verbose_name_plural': 'Comercio',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_payment', models.CharField(max_length=100, verbose_name='ID del pago')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Monto')),
                ('currency', models.CharField(max_length=50, verbose_name='Moneda de cambio')),
                ('reference_num', models.CharField(max_length=100, verbose_name='Numero de referencia')),
                ('reference', models.CharField(max_length=100, verbose_name='Referencia')),
                ('type', models.CharField(max_length=100, verbose_name='Tipo')),
                ('type_description', models.CharField(max_length=100, verbose_name='Descripcion de tipo')),
                ('wallet', models.CharField(max_length=100, verbose_name='Cartera')),
                ('id_wallet', models.CharField(max_length=100, verbose_name='ID de la cartera')),
            ],
            options={
                'verbose_name_plural': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='Qr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr', models.CharField(max_length=50, verbose_name='QR ID')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripcion')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Monto')),
                ('currency', models.CharField(max_length=20, verbose_name='Mondeda de cambio')),
                ('reference_num', models.CharField(max_length=50, verbose_name='Número de referencia')),
            ],
            options={
                'verbose_name_plural': 'QR',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_refunds', models.CharField(max_length=100, verbose_name='ID del reembolso')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)], verbose_name='Monto del reembolso')),
                ('currency', models.CharField(max_length=10, verbose_name='Moneda de cambio')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name_plural': 'Refund',
            },
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=100, verbose_name='Empleado')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre de terminal')),
            ],
            options={
                'verbose_name_plural': 'Terminal',
            },
        ),
        migrations.CreateModel(
            name='UbicacionT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.category', verbose_name='ID de la categoria')),
                ('id_mer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.merchant', verbose_name='ID del comercio')),
            ],
            options={
                'verbose_name_plural': 'Ubicacion de la tienda',
            },
        ),
        migrations.CreateModel(
            name='RealizarP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_ticket', models.CharField(max_length=50, verbose_name='ID del ticket')),
                ('currency', models.CharField(max_length=50, verbose_name='Moneda de cambio')),
                ('reference', models.CharField(max_length=50, verbose_name='Numero de referencia')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('refunded', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)], verbose_name='Reembolso')),
                ('id_cashout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.cashoutm', verbose_name='ID del retiro')),
                ('id_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.category', verbose_name='ID de la categoria')),
                ('id_create', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.createpay', verbose_name='ID de la creacion del pago')),
                ('id_merch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.merchant', verbose_name='ID del comercio')),
                ('id_pay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.payment', verbose_name='ID del pago')),
                ('id_qr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.qr', verbose_name='ID de QR')),
                ('id_refunds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.refund', verbose_name='ID del reembolso')),
                ('id_terminal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.terminal', verbose_name='ID de la terminal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Realizar pago',
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=50, verbose_name='ID de la info')),
                ('id_cash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.cashoutm', verbose_name='ID del retiro')),
                ('id_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.category', verbose_name='ID de la categoria')),
                ('id_mer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.merchant', verbose_name='ID del comercio')),
                ('id_qr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.qr', verbose_name='QR ID')),
            ],
            options={
                'verbose_name_plural': 'Informacion del cobro',
            },
        ),
        migrations.AddField(
            model_name='createpay',
            name='id_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.info', verbose_name='ID Info cobro'),
        ),
        migrations.AddField(
            model_name='createpay',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dapp.payment', verbose_name='ID Payment'),
        ),
        migrations.AddField(
            model_name='createpay',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]

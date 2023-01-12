# Generated by Django 3.2.16 on 2023-01-12 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banca', '0028_nivelcuenta'),
        ('demograficos', '0063_operacionesmensual_origendeposito_perfiltransaccionaldeclarado_transferenciasmensuales_usocuenta'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nivel_cuenta',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='banca.nivelcuenta'),
        ),
    ]

# Generated by Django 3.2 on 2023-02-24 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pld', '0003_auto_20230221_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mensaje',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
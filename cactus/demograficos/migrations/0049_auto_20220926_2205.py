# Generated by Django 3.2 on 2022-09-27 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0048_auto_20220713_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='kitComisiones',
            field=models.FileField(blank=True, null=True, upload_to='docs/pdfLegal'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='kitDeclaraciones',
            field=models.FileField(blank=True, null=True, upload_to='docs/pdfLegal'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='kitPrivacidad',
            field=models.FileField(blank=True, null=True, upload_to='docs/pdfLegal'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='kitTerminos',
            field=models.FileField(blank=True, null=True, upload_to='docs/pdfLegal'),
        ),
    ]

# Generated by Django 2.2.8 on 2022-07-02 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0046_auto_20220630_1316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='kaySource',
            new_name='keySource',
        ),
    ]

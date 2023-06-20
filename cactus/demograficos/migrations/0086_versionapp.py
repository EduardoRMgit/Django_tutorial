# Generated by Django 3.2 on 2023-05-26 23:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0085_cancelacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='VersionApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=2056)),
                ('activa', models.BooleanField(default=True)),
                ('url_android', models.URLField(blank=True, null=True)),
                ('url_ios', models.URLField(blank=True, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
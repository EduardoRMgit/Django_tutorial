# Generated by Django 3.2 on 2023-04-26 20:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('demograficos', '0076_auto_20230410_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenDinamico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=10)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_tokenD', to='demograficos.userprofile')),
            ],
        ),
    ]

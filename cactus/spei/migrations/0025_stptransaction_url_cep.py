# Generated by Django 3.2 on 2023-06-28 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spei', '0024_auto_20220926_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='stptransaction',
            name='url_cep',
            field=models.URLField(blank=True, max_length=2056, null=True),
        ),
    ]
# Generated by Django 3.0.3 on 2020-04-06 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200405_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='secret',
            field=models.BooleanField(default=False),
        ),
    ]

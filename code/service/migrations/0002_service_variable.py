# Generated by Django 3.0.3 on 2020-04-03 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200403_1538'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='variable',
            field=models.ManyToManyField(blank=True, default='', to='store.Variable'),
        ),
    ]

# Generated by Django 3.0.3 on 2020-04-04 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='container_image',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]

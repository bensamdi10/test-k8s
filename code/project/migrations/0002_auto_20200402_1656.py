# Generated by Django 3.0.3 on 2020-04-02 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='provider',
            field=models.CharField(choices=[('Google_cloud', 'Google Cloud'), ('aws', 'AWS'), ('heroku', 'Heroku'), ('digital_ocean', 'Digital Ocean'), ('minikube', 'Minikube')], max_length=200),
        ),
    ]

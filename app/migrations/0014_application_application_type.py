# Generated by Django 4.2.11 on 2024-04-19 22:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_applicationuser_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_type',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.1.7 on 2021-03-19 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='active',
        ),
    ]
# Generated by Django 3.1.3 on 2021-01-16 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210115_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='network_requests',
        ),
    ]

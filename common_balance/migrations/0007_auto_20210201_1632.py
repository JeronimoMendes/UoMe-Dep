# Generated by Django 3.1.5 on 2021-02-01 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_balance', '0006_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

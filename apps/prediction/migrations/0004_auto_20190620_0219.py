# Generated by Django 2.0.13 on 2019-06-20 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0003_auto_20190620_0217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weeklyprediction',
            old_name='simulate_return',
            new_name='sim_return',
        ),
    ]

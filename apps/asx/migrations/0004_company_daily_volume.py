# Generated by Django 2.0.13 on 2019-06-19 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asx', '0003_auto_20190618_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='daily_volume',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True, verbose_name='daily volume'),
        ),
    ]

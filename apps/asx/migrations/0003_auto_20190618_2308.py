# Generated by Django 2.0.13 on 2019-06-18 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asx', '0002_company_asx_200'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='last_price',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='last price'),
        ),
        migrations.AddField(
            model_name='company',
            name='last_price_date',
            field=models.DateField(blank=True, null=True, verbose_name='last price date'),
        ),
    ]

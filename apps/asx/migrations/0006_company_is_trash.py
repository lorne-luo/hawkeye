# Generated by Django 2.0.13 on 2019-06-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asx', '0005_company_create_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_trash',
            field=models.BooleanField(default=False),
        ),
    ]

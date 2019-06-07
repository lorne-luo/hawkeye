# Generated by Django 2.0.13 on 2019-06-07 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailstreamforms', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedFormSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_address', models.EmailField(blank=True, max_length=254)),
                ('from_address', models.EmailField(blank=True, max_length=254)),
                ('form', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='advanced_settings', to='wagtailstreamforms.Form')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
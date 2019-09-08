# Generated by Django 2.1.7 on 2019-09-08 22:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='nombre')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='año')),
                ('subgroups', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='número de subgrupos')),
                ('telegram_group', models.CharField(blank=True, default='', max_length=64, verbose_name='grupo telegram')),
                ('telegram_channel', models.CharField(blank=True, default='', max_length=64, verbose_name='canal telegram')),
            ],
            options={
                'verbose_name': 'grupo',
            },
        ),
        migrations.AlterField(
            model_name='subject',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='año'),
        ),
    ]

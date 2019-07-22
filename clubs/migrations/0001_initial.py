# Generated by Django 2.1.7 on 2019-07-19 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('name', models.CharField(max_length=64, verbose_name='nombre')),
                ('slug', models.SlugField(max_length=64, primary_key=True, serialize=False, verbose_name='slug')),
                ('description', models.TextField(max_length=300, verbose_name='descripción')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='gestor')),
            ],
        ),
        migrations.CreateModel(
            name='ClubMeeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='título')),
                ('place', models.CharField(max_length=120, verbose_name='lugar')),
                ('moment', models.DateTimeField(verbose_name='fecha')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.Club', verbose_name='club')),
            ],
        ),
    ]
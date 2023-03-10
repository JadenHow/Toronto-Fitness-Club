# Generated by Django 4.0.1 on 2022-12-09 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('studios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=120, null=True)),
                ('coach', models.CharField(max_length=120, null=True)),
                ('keywords', models.CharField(max_length=120, null=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('end_recursion', models.DateField()),
                ('cancelled', models.BooleanField(default=False)),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studios.studio')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='ClassInstances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=120, null=True)),
                ('coach', models.CharField(max_length=120, null=True)),
                ('keywords', models.CharField(max_length=120, null=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('currently_enrolled', models.PositiveIntegerField(default=0)),
                ('class_date', models.DateField()),
                ('class_date_timestamp', models.IntegerField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('start_time_timestamp', models.IntegerField(blank=True, null=True)),
                ('end_time', models.TimeField()),
                ('cancelled', models.BooleanField(default=False)),
                ('parent_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studios.studio')),
            ],
            options={
                'verbose_name': 'Class Instance',
                'verbose_name_plural': 'Class Instances',
            },
        ),
    ]

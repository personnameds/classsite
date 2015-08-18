# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('number', models.PositiveSmallIntegerField(verbose_name='Perod #')),
                ('start_time', models.CharField(max_length='5')),
                ('end_time', models.CharField(max_length='5')),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
            },
        ),
        migrations.CreateModel(
            name='Recess_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('number', models.PositiveSmallIntegerField(verbose_name='Recess #')),
                ('start_time', models.CharField(max_length='5')),
                ('end_time', models.CharField(max_length='5')),
            ],
            options={
                'verbose_name': 'Recess',
                'verbose_name_plural': 'Recesses',
            },
        ),
        migrations.CreateModel(
            name='Schedule_Setup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('days_in_cycle', models.PositiveSmallIntegerField(verbose_name='Days in a cycle')),
                ('lunch_start', models.CharField(verbose_name='Lunch Start', max_length='5')),
                ('lunch_end', models.CharField(verbose_name='Lunch End', max_length='5')),
                ('before_start', models.CharField(verbose_name='Before Start', max_length='5')),
                ('before_end', models.CharField(verbose_name='Before End', max_length='5')),
                ('after_start', models.CharField(verbose_name='After Start', max_length='5')),
                ('after_end', models.CharField(verbose_name='After End', max_length='5')),
            ],
            options={
                'verbose_name': 'Schedule Setup',
                'verbose_name_plural': 'Schedule Setup',
            },
        ),
        migrations.AddField(
            model_name='recess_details',
            name='schedule',
            field=models.ForeignKey(to='schoolsetup.Schedule_Setup'),
        ),
        migrations.AddField(
            model_name='period_details',
            name='schedule',
            field=models.ForeignKey(to='schoolsetup.Schedule_Setup'),
        ),
    ]

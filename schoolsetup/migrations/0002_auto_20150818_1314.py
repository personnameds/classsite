# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsetup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period_details',
            name='end_time',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='period_details',
            name='start_time',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='recess_details',
            name='end_time',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='recess_details',
            name='start_time',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='after_end',
            field=models.CharField(verbose_name='After End', max_length=5),
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='after_start',
            field=models.CharField(verbose_name='After Start', max_length=5),
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='before_end',
            field=models.CharField(verbose_name='Before End', max_length=5),
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='before_start',
            field=models.CharField(verbose_name='Before Start', max_length=5),
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='lunch_end',
            field=models.CharField(verbose_name='Lunch End', max_length=5),
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='lunch_start',
            field=models.CharField(verbose_name='Lunch Start', max_length=5),
        ),
    ]

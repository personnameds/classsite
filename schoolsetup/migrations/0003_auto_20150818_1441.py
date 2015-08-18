# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsetup', '0002_auto_20150818_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule_setup',
            name='periods_in_day',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='Periods in a Day'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule_setup',
            name='days_in_cycle',
            field=models.PositiveSmallIntegerField(verbose_name='Days in a Cycle'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('day_no', '0002_auto_20150818_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day_no',
            options={'verbose_name': 'Day #'},
        ),
        migrations.AddField(
            model_name='period',
            name='day_no',
            field=models.ForeignKey(to='day_no.Day_No', default=1, verbose_name='Day #'),
            preserve_default=False,
        ),
    ]

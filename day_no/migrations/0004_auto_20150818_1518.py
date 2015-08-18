# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('day_no', '0003_auto_20150818_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='modified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='period',
            name='details',
            field=models.ForeignKey(verbose_name='Period #', to='schoolsetup.Period_Details'),
        ),
    ]

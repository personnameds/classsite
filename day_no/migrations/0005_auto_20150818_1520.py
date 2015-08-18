# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('day_no', '0004_auto_20150818_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='modified',
            field=models.BooleanField(default=False, verbose_name='Modified'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsetup', '0003_auto_20150818_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='period_details',
            options={'verbose_name_plural': 'Period Details', 'verbose_name': 'Period Details'},
        ),
        migrations.AlterModelOptions(
            name='recess_details',
            options={'verbose_name_plural': 'Recess Details', 'verbose_name': 'Recess Details'},
        ),
    ]

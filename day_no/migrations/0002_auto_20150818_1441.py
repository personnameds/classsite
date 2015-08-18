# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('day_no', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day_no',
            name='klass',
            field=models.ForeignKey(verbose_name='Class', to='classlists.Klass'),
        ),
    ]

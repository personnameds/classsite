# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolsetup', '__first__'),
        ('classlists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day_No',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('day_name', models.CharField(max_length=2)),
                ('klass', models.ForeignKey(to='classlists.Klass', verbose_name='Class')),
            ],
            options={
                'verbose_name': 'Day #',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('activity', models.CharField(max_length=12)),
                ('modified', models.BooleanField(default=False, verbose_name='Modified')),
                ('day_no', models.ForeignKey(to='day_no.Day_No', verbose_name='Day #')),
                ('details', models.ForeignKey(to='schoolsetup.Period_Details', verbose_name='Period #')),
            ],
        ),
    ]

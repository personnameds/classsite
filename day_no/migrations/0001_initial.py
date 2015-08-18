# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classlists', '0001_initial'),
        ('schoolsetup', '0002_auto_20150818_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day_No',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day_name', models.CharField(max_length=2)),
                ('klass', models.ForeignKey(to='classlists.Klass')),
            ],
            options={
                'verbose_name': 'Day Number',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('activity', models.CharField(max_length=12)),
                ('details', models.ForeignKey(to='schoolsetup.Period_Details')),
            ],
        ),
    ]

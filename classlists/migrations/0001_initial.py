# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('klass_name', models.CharField(unique=True, verbose_name='Class', max_length=12)),
                ('klass_code', models.CharField(verbose_name='Class Code', max_length=10)),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='School_Staff',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('teacher_name', models.CharField(unique=True, max_length=20)),
                ('allow_contact', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('klass', models.ForeignKey(verbose_name='Class', to='classlists.Klass')),
                ('user', models.OneToOneField(verbose_name='User Name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 07:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0008_auto_20170912_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 9, 12, 7, 56, 53, 833814)),
        ),
    ]

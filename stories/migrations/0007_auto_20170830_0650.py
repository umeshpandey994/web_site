# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0006_auto_20170830_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
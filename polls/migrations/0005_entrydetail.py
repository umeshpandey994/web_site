# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20170817_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.Entry2')),
            ],
        ),
    ]

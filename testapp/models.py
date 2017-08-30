# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class T1(models.Model):
    name = models.CharField(max_length=20)


class T2(models.Model):
    t1 = models.ManyToManyField(T1)
    name = models.CharField(max_length=40)




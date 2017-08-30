# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from subscribers.models import Company


class Source(models.Model):
    created_by = models.ForeignKey(User, related_name="source_created")
    updated_by = models.ForeignKey(User, related_name="source_updated",
                                   default=28)
    companies = models.ManyToManyField(Company)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=255)

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = (("url", "created_by"),)




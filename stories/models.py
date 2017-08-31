# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from sourcelisting.models import Source
from subscribers.models import Company


class Story(models.Model):
    company = models.ManyToManyField(Company, related_name="stories_company")
    source = models.ForeignKey(Source)
    client = models.ForeignKey(Company, related_name="story_client")

    created_by = models.ForeignKey(User, related_name="stories_created_by",
                                   default=28)
    updated_by = models.ForeignKey(User, related_name="story_updated_by",
                                   default=28)

    title = models.CharField(max_length=250)
    url = models.URLField(max_length=255)
    pub_date = models.DateTimeField()
    body_text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ("url", "source")


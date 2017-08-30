# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    created_by = models.ForeignKey(User, related_name="companies_created_by")
    updated_by = models.ForeignKey(User, related_name="companies_updated_by")

    name = models.CharField(max_length=100)
    url = models.URLField(max_length=255, unique=True,null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)


class Subscriber(models.Model):
    user = models.OneToOneField(User, related_name='subscriber_user')
    created_by = models.ForeignKey(User, related_name="subscriber_created_by",
                                   default=28)
    updated_by = models.ForeignKey(User, related_name="subscriber_updated_by",
                                   default=28)

    company = models.ForeignKey(Company, related_name='company_name')
    client = models.ForeignKey(Company, related_name='client_name')
    #gender = models.IntegerField(max_length=1, null=True)
    hobbies = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)



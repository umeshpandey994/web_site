# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stories import views

from django.conf.urls import url

urlpatterns = [

        url(r'^addstory/$', views.addstory),
]
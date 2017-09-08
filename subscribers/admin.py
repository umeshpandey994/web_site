# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.contrib.admin import FieldListFilter
from django.contrib.admin import SimpleListFilter
from django.urls import reverse

from subscribers.models import Subscriber, Company

import re


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = "__all__"

    def clean(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'[a-zA-Z ]+',name):
            raise forms.ValidationError({'name': "Name should be alphabetic"})

        return self.cleaned_data


class CompanyAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('is_active__exact'):
            q = request.GET.copy()
            q['is_active__exact'] = '1'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(CompanyAdmin, self).changelist_view(request,extra_context=extra_context)

    form = CompanyForm
    fieldsets = (
        (None,{
            'fields': (('name', 'url'), 'created_by', 'updated_by', 'is_active')

    }),
                 )
    list_display = ('name', 'url','created_by', 'updated_by')
    list_filter = ('is_active', 'created_by')
    search_fields = ('^name', '^url')


admin.site.register(Subscriber)
admin.site.register(Company, CompanyAdmin)



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from sourcelisting.models import Source
from subscribers.models import Company


class CompaniesInLine(admin.TabularInline):
    model = Source.companies.through


class SourceAdmin(admin.ModelAdmin):
    template = "admin/sourcelisting/source/change_list.html"
    list_display = ('name', 'test_popup', 'aid_link', 'url', 'created_by', 'updated_by')
    save_on_top = True
    fieldsets = (
        ('group1',{
            'fields': ('name', 'url')
        }),
        ('group2',{
            'fields': ('companies',)
        }),
        ('group3',{
            'fields': ('created_by', 'updated_by')
        })
    )
    #raw_id_fields = ('source',)
    inlines = [CompaniesInLine]

admin.site.register(Source, SourceAdmin)

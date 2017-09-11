# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from stories.models import Story


class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'body_text', 'pub_date')
    fieldsets = (
        ('group 1',{
            'fields': ('title', 'url', 'pub_date', 'body_text')
        }),
        ('group2',{
            'fields': ('source', 'company', 'client')
        }),
        ('group3',{
            'fields': ('created_by', 'updated_by')
        })
    )
    save_on_top = True
admin.site.register(Story, StoryAdmin)
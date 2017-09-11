# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.contrib.auth.models import User

from subscribers.models import Subscriber, Company
from sourcelisting.models import Source

import re

admin.site.disable_action('delete_selected')


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = "__all__"

    def clean(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'[a-zA-Z ]+',name):
            raise forms.ValidationError({'name': "Name should be alphabetic"})

        return self.cleaned_data


class custom_filter_created_by(admin.SimpleListFilter):
    title = 'created_by'
    parameter_name = "created_by_id"

    def lookups(self, request, model_admin):
        users_name = []
        qs = User.objects.filter(is_staff=True)
        for i in qs:
            users_name.append((i.id, i.username))
        return tuple(users_name)

    def queryset(self, request, queryset):
        if self.value() !=  None:
            queryset = queryset.filter(created_by_id=self.value())
        return queryset


class SubscriberInLine(admin.TabularInline):
    model = Subscriber
    readonly_fields = ('getFirst_name', 'getLast_name')
    fieldsets = (
        (
            None, {
                'fields': ('getLast_name',)
            }
        ),
        (
            'Group 2', {
                'fields': ('created_by', 'updated_by'),
            }
        ),

    )

    fk_name = "company"

    def getFirst_name(self, obj):
        print obj.user.first_name
        return obj.user.username
    getFirst_name.allow_tags = True

    def getLast_name(self, obj):
        return obj.user.last_name
    getLast_name.allow_tags = True



class CompaniesInLine(admin.TabularInline):
    model = Source.companies.through


class CompanyAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        #print request
        if not request.GET.has_key('is_active__exact'):
            q = request.GET.copy()
            q['is_active__exact'] = '1'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(CompanyAdmin, self).changelist_view(request,
                                                         extra_context =
                                                         extra_context
                                                         )

    form = CompanyForm

    fieldsets = (
        (
            'Group 1', {
                'fields': ('name', 'url')
            }
        ),
        (
            'Group 2', {
                'fields':  ('created_by', 'updated_by'),
            }
        ),
        (
            'Group 3', {
                'fields': ('is_active',)
            }
        ),
    )

    inlines = [SubscriberInLine, CompaniesInLine]

    list_display = ('name', 'url','created_by', 'updated_by')

    list_filter = ('is_active', custom_filter_created_by)

    search_fields = ('^name', '^url')

    actions_on_bottom = True

    actions_on_top = False

    actions = ["inactive"]

    list_editable = ('name',)

    list_display_links = ('url', 'created_by', 'updated_by')

    save_on_top = True

    def inactive(self, request, queryset):
        print request
        for qs in queryset:
            qs.is_active = False
            qs.save()


class SubscriberAdmin(admin.ModelAdmin):

    list_display = ('user', 'company_name', 'client_name', 'created_by',
                    'updated_by')

    def company_name(self, obj):
        return obj.company.name

    def client_name(self, obj):
        return obj.company.name
    list_filter = ('user',)
    save_on_top = True
    fieldsets = (
        ('group1', {
            'fields': ('user', 'company', 'client')
        }),
        ('group2', {
            'fields': ('created_by', 'updated_by')
        }),
    )

admin.site.register(Company, CompanyAdmin)
admin.site.register(Subscriber, SubscriberAdmin)



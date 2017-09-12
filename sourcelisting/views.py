# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from dateutil.parser import parse
from sourcelisting.models import Source
from subscribers.models import Company,Subscriber
from stories.models import Story

import requests
from bs4 import BeautifulSoup
from datetime import datetime


import feedparser
import re


def filterdata(data):
    p = re.compile(r'<.+>')
    return p.sub('', data)


def add_source(request):
    cxt = {
        'name_error': "Please Insert Name",
        'url_error': "Please Enter URL",
    }
    if request.method == "POST":
        name = request.POST['name']
        url = request.POST['url']
        companies_id = request.POST.getlist("companies_id")
        if name is None:
            return render(request, "sourcelisting/add.html", cxt['name_error'])
        elif url is None:
            return render(request, "sourcelisting/add.html", cxt['url_error'])
        else:
            source = Source()
            source.name = name
            source.url = url
            source.created_by_id = request.user.id
            source.save()
            li = list(map(int, companies_id))
            source.companies.add(*li)
            source = Source.objects.filter(created_by=request.user)
            cxt = {
                'qs': source.values('name', 'url', 'id')
            }
            return render(request, 'sourcelisting/listing.html', cxt)
    else:
        company = Company.objects.filter(is_active=True)
        cxt = {
            'qs': company.values('name', 'id')
        }
        return render(request, 'sourcelisting/add.html', cxt)


@csrf_exempt
def delete_source(request,del_id):
        Source.objects.get(id=del_id).delete()
        source = Source.objects.filter(created_by=request.user)
        cxt = {
            'qs': source.values('name', 'url', 'id')
        }
        return render(request, "sourcelisting/listing.html", cxt)


def edit_source(request,edit_id):
    source = Source.objects.get(id=edit_id)
    cxt = {
        'error': "Please Enter Data Properly"
    }
    if request.method == 'POST':
        name = request.POST['name']
        url = request.POST['url']
        if name is None or url is None:
            return render(request, "sourcelisting/edit.html", cxt)
        else:
            source.name = name
            source.url = url
            source.save()
            s = Source.objects.filter(created_by=request.user)
            cxt = {
                'qs': s.values('name', 'url', 'id')
            }
            return render(request, "sourcelisting/listing.html", cxt )
    else:
        qs = {'name': source.name, 'url': source.url}
        return render(request, "sourcelisting/edit.html", {'qs': qs})


def fetch_stories(request, id):
    if request.method == "GET":
        source = Source.objects.filter(created_by=request.user)
        fetch(id)
        cxt = {
            'qs': source.values('name', 'url', 'id')
        }
        return render(request, 'sourcelisting/listing.html', cxt)
    else:
        return HttpResponse("data not saved into database")


def listing(request):
    source = Source.objects.filter(created_by=request.user)
    cxt = {
        'qs': source.values('name', 'url', 'id')
    }
    return render(request, "sourcelisting/listing.html", cxt)


def search_source(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
        search = Source.objects.filter(name=search_text,
                                       created_by=request.user)
        source = Source.objects.filter(created_by=request.user)
        cxt = {
            'qs1': search.values('name', 'url'),
            'qs': source.values('name', 'url', 'id')

        }
        return render(request, "sourcelisting/listing.html", cxt)


def fetchall(request):
    if request.method == 'GET':
        source = Source.objects.filter(created_by=request.user)
        cxt = {
            'qs': source.values('name', 'url', 'id')
        }
        for i in source:
            fetchstory(i.id)
        return render(request, 'sourcelisting/listing.html', cxt)


def fetchstory(id):
    source = Source.objects.get(id=id)
    f = feedparser.parse(source.url)
    for entry in f.entries:
        if Story.objects.filter(url__exact=entry.link, source=id).exists():
            pass
        else:
            s = Story()
            s.url = entry.link
            s.title = entry.title
            dt = parse(str(entry.published))
            s.pub_date = dt
            s.body_text = filterdata(entry.summary)
            s.source_id = id
            s.client_id = source.created_by.subscriber_user.client_id
            s.save()
            list_companies = source.companies.values_list('id', flat=True)
            story_obj = Story.objects.get(id=s.id)
            story_obj.company.add(*list_companies)


# def fetchstory(id):
#     source = Source.objects.get(id=id)
#     r = requests.get(source.url)
#     xml_doc = r.content
#     soup = BeautifulSoup(xml_doc, "xml")
#
#     for t in soup.find_all('item'):
#         if Story.objects.filter(url__exact=t.find('link').string,
#                                 source=id).exists():
#             pass
#         else:
#             s = Story()
#             s.url = t.find('link').string
#             s.title = t.find('title').string
#             if t.find('pubDate') is not None:
#                 s.pub_date = parse(t.find('pubDate').string)
#             else:
#                 s.pub_date = datetime.now()
#             s.body_text = filterdata(t.find('description').string)
#             s.source_id = id
#             s.client_id = source.created_by.subscriber_user.client_id
#             s.save()
#             list_companies = source.companies.values_list('id', flat=True)
#             story_obj = Story.objects.get(id=s.id)
#             story_obj.company.add(*list_companies)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from dateutil.parser import parse

from sourcelisting.models import Source
from subscribers.models import Company,Subscriber
from stories.models import Story

import feedparser


def add(request):
    if request.method == "POST":
        name = request.POST['name']
        url = request.POST['url']
        companies = request.POST.getlist("companies")
        created_by = request.user.id
        source = Source()
        source.name = name
        source.url = url
        source.created_by_id = created_by
        source.save()
        qs1 = Source.objects.get(id=source.id)
        qs = Source.objects.filter(created_by=created_by)
        li = list(map(int, companies))
        for i in li:
            qs1.companies.add(i)
        return render(request, 'sourcelisting/listing.html', {'qs': qs})
    else:
        qs = Company.objects.all()
        return render(request, 'sourcelisting/add.html', {'qs': qs})


@csrf_exempt
def delete(request,del_id):
        qs1 = Source.objects.get(id=del_id)
        qs1.delete()
        created_by = request.user.id
        qs = Source.objects.filter(created_by=created_by)
        return render(request, "sourcelisting/listing.html", {'qs': qs})


def edit(request,edit_id):
    if request.method == 'POST':
        name = request.POST['name']
        url = request.POST['url']
        qs1 = Source.objects.get(id=edit_id)
        qs1.name = name
        qs1.url = url
        qs1.save()
        created_by = request.user.id
        qs = Source.objects.filter(created_by=created_by)
        return render(request, "sourcelisting/listing.html",{'qs': qs} )
    else:
        qs = Source.objects.get(id=edit_id)
        return render(request, "sourcelisting/edit.html", {'qs': qs})


def fetch_stories(request, id):
    if request.method == "GET":
        qs1 = Source.objects.get(id=id)
        qs = Source.objects.filter(created_by=qs1.created_by_id)
        f = feedparser.parse(qs1.url)
        for entry in f.entries:
                s = Story()
                s.title = entry.title
                s.url = entry.link
                dt = parse(str(entry.published))
                s.pub_date = "{}-{}-{} {}:{}:{}".format(dt.year, dt.month,
                                                        dt.day, dt.hour,
                                                        dt.minute, dt.second
                                                        )
                s.body_text = entry.summary
                s.source_id = id
                qs2 = Subscriber.objects.get(user_id=qs1.created_by_id)
                s.client_id = qs2.client_id
                try:
                    s.save()
                except:
                     pass
                list_companies = qs1.companies.values_list('id', flat=True)
                story_obj = Story.objects.get(id=s.id)
                for i in list_companies:
                    story_obj.company.add(i)
        return render(request, 'sourcelisting/listing.html', {"qs": qs})
    else:
        return HttpResponse("data not saved into db")


def listing(request):
    qs = Source.objects.filter(created_by=request.user.id)
    return render(request, "sourcelisting/listing.html", {'qs': qs})





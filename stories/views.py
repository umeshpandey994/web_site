# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from subscribers.models import Company,Subscriber
from sourcelisting.models import Source
from stories.models import Story


def addstory(request):
    user_id = request.user.id
    cxt = {
        'company_qs': Company.objects.all(),
        'source_qs': Source.objects.filter(created_by=user_id),
    }
    if request.method == "POST":
        title = request.POST.get('title')
        pub_date = request.POST.get('pub_date')
        body_text = request.POST.get('body_text')
        url = request.POST.get('url')
        companies = request.POST.getlist('companies')
        # client = request.POST.get('client')
        source = request.POST.get('source')

        s = Story()
        s.title = title
        s.source_id = source
        s.pub_date = pub_date
        s.body_text = body_text
        s.url = url
        client = Subscriber.objects.get(user_id= user_id)
        s.client_id = client.client_id
        s.save()
        li = map(int, companies)
        for company in li:
            s.company.add(company)
        return render(request, 'stories/showstories.html', )
    else:
        return render(request, 'stories/addstory.html', cxt)


def source(request, story):
    qs = Source.objects.get(id=story)
    return qs.name


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

from subscribers.models import Company,Subscriber
from sourcelisting.models import Source
from stories.models import Story

from dateutil.parser import parse


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


def edit_story(request, edit_id):
    cxt = {
        'qs': Story.objects.get(id=edit_id),
        'company_qs': Company.objects.all(),
        'source_qs': Source.objects.filter(created_by=request.user.id)
    }
    if request.method == "POST":
        title = request.POST['title']
        url = request.POST['url']
        pub_date = request.POST['pub_date']
        body_text = request.POST['body_text']
        source = request.POST['source']
        companies = request.POST.getlist('companies')
        cxt['qs'].title = title
        cxt['qs'].url = url
        dt = parse(str(pub_date))
        cxt['qs'].pub_date = "{}-{}-{} {}:{}:{}".format(dt.year, dt.month,
                                                        dt.day, dt.hour,
                                                        dt.minute, dt.second
                                                        )
        cxt['qs'].body_text = body_text
        cxt['qs'].source_id = source
        cxt['qs'].save()
        for company in map(int, companies):
            cxt['qs'].company.add(company)

        sub = Subscriber.objects.get(user_id=request.user.id)
        client = sub.client_id
        qs = Story.objects.filter(client=client)
        if qs.exists():
            return render(request, "stories/showstories.html",
                          {'qs': qs}
                          )
    else:
        return render(request, "stories/edit.html", cxt)


def delete_story(request, delete_id):
    qs = Story.objects.get(id=delete_id)
    qs.delete()
    sub = Subscriber.objects.get(user_id=request.user.id)
    client = sub.client_id
    qs = Story.objects.filter(client=client)
    if qs.exists():
        return render(request, "stories/showstories.html",
                      {'qs': qs}
                      )


def search(request):
    if request.method == "GET":
        search_text = request.GET['search_box']

        sub = Subscriber.objects.get(user_id=request.user.id)
        client = sub.client_id
        cxt = {
            'qs1': Story.objects.filter(title=search_text),
            'qs': Story.objects.filter(client=client)
        }
        cxt['qs1'].count()
        return render(request, "stories/showstories.html", cxt)

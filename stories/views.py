# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from subscribers.models import Company
from sourcelisting.models import Source
from stories.models import Story

from dateutil.parser import parse


def addstory(request):
    company = Company.objects.filter(is_active=True)
    source = Source.objects.filter(created_by=request.user)
    story = Story.objects.filter(client_id=request.user.subscriber_user.client_id)
    qs = []
    for i in story:
        qs.append({'title': i.title, 'url': i.url, 'pub_date': i.pub_date,
                   'body_text': i.body_text, 'id':i.id,
                   'company__name': i.company.all(),
                   'source__name': i.source.name})

    cxt = {
        'company_qs': company.values('name', 'id'),
        'source_qs': source.values('name', 'id'),

        # 'qs': story.values('title', 'pub_date', 'url', 'body_text',
        #                    'source__name', 'id', 'company__name'),
    }
    cxt1 = {
        'title_error': "Please Enter Title",
        'url_error': "Please Enter URL"
    }
    if request.method == "POST":
        title = request.POST.get('title')
        pub_date = request.POST.get('pub_date')
        body_text = request.POST.get('body_text')
        url = request.POST.get('url')
        companies_id = request.POST.getlist('companies_id')
        source_id = request.POST.get('source_id')
        if title is None:
            return render(request, 'stories/addstory.html', cxt1['title_error'])
        elif url is None:
            return render(request, 'stories/addstory.html', cxt1['url_error'])
        else:
            s = Story()
            s.title = title
            s.source_id = source_id
            s.pub_date = pub_date
            s.body_text = body_text
            s.url = url
            s.client_id = request.user.subscriber_user.client_id
            s.save()
            li = map(int, companies_id)
            s.company.add(*li)
            return render(request, 'stories/showstories.html', {'qs': qs})
    else:
        return render(request, 'stories/addstory.html', cxt)


def edit_story(request, edit_id):
    cxt = {
        'qs': Story.objects.get(id=edit_id),
        'company_qs': Company.objects.filter(is_active=True),
        'source_qs': Source.objects.filter(created_by=request.user)
    }
    if request.method == "POST":
        title = request.POST['title']
        url = request.POST['url']
        pub_date = request.POST['pub_date']
        body_text = request.POST['body_text']
        source = request.POST.get('source')
        companies_id = request.POST.getlist('companies_id')
        cxt['qs'].title = title
        cxt['qs'].url = url
        dt = parse(str(pub_date))
        cxt['qs'].pub_date = dt
        cxt['qs'].source_id = source
        cxt['qs'].body_text = body_text
        cxt['qs'].save()
        for company in map(int, companies_id):
            cxt['qs'].company.add(company)

        # sub = Subscriber.objects.get(user_id=request.user.id)
        # client = sub.client_id
        # showstories change in source and company
        story = Story.objects.filter(client=request.user.subscriber_user.client)
        if story.exists():
            qs = []
            for i in story:
                qs.append(
                    {
                     'title': i.title, 'url': i.url, 'pub_date': i.pub_date,
                     'body_text': i.body_text, 'id': i.id,
                     'company__name': i.company.all(),
                     'source__name': i.source.name
                    }
                )
            return render(request, "stories/showstories.html", {'qs': qs})
    else:
        return render(request, "stories/edit.html", cxt)


def delete_story(request, delete_id):
    Story.objects.get(id=delete_id).delete()
    # sub = Subscriber.objects.get(user_id=request.user.id)
    # client = sub.client_id
    story = Story.objects.filter(client=request.user.subscriber_user.client)
    if story.exists():
        qs = []
        for i in story:
            qs.append({'title': i.title, 'url': i.url, 'pub_date': i.pub_date,
                       'body_text': i.body_text, 'id': i.id,
                       'company__name': i.company.all(),
                       'source__name': i.source.name})

        return render(request, "stories/showstories.html", {'qs': qs}
                      )


def search(request):
    if request.method == "GET":
        search_text = request.GET['search_box']
        search = Story.objects.filter(title=search_text)
        story = Story.objects.filter(client=request.user.subscriber_user.client)
        #cxt['qs1'].count()
        qs = []
        for i in story:
            qs.append({'title': i.title, 'url': i.url, 'pub_date': i.pub_date,
                       'body_text': i.body_text, 'id': i.id,
                       'company__name': i.company.all(),
                       'source__name': i.source.name})

        cxt = {
            'qs1': search.values('title', 'url'),
            # 'qs': story.values('title', 'url', 'pub_date', 'body_text',
            #                    'source__name', 'company__name', 'id')
        }
        return render(request, "stories/showstories.html", {'qs': qs})


def delete_company(request, delete_id, company_name):
    cxt = {
        'qs': Story.objects.get(id=delete_id),
        'company_qs': Company.objects.filter(is_active=True),
        'source_qs': Source.objects.filter(created_by=request.user)
    }
    qs2 = Story.objects.get(id=delete_id)
    qs1 = qs2.company.get(name=company_name)
    qs2.company.remove(qs1.id)
    return HttpResponseRedirect(reverse('editstory', args=(delete_id,)))




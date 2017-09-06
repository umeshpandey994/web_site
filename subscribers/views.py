# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.auth import authenticate,login
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from stories.models import Story
from subscribers.models import Company,Subscriber


@csrf_protect
def signup(request):
    cxt = {
        'company_qs': Company.objects.filter(is_active=True),
    }
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        company_id = request.POST['company']
        client_id = request.POST['client']
        gender = request.POST['gender']
        # hobbies = ','.join(request.POST.getlist('hobbies'))
        user_qs = User.objects.filter(username__exact=username)

        if user_qs.exists():
            cxt['error'] = "Username Already Exist"
            return render(request, 'subscribers/signup.html', cxt)
        elif password != confirm_password:
            cxt['error'] = "Password Invalid"
            return render(request, 'subscribers/signup.html', cxt)
        else:
            # user = User.objects.create_user(username=username,
            #                                 email=email,
            #                                 password=password,
            #                                 first_name=first_name,
            #                                last_name=last_name)
            user = User()
            user.username = username
            user.first_name = first_name,
            user.last_name = last_name
            user.email = email
            user.set_password(password)
            try:
                user.save()
            except DatabaseError as e:

                raise ValidationError(e)
            sub = Subscriber()
            sub.company_id = company_id
            sub.client_id = client_id
            sub.user = user
            sub.gender = gender
            # sub.hobbies = hobbies
            try:
                sub.save()
            except DatabaseError as e:
                raise ValidationError(e)
            return HttpResponseRedirect("/page/login")
    else:
        return render(request, 'subscribers/signup.html', cxt)


@csrf_exempt
def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.source_created.exists():
                story = Story.objects.filter(client=user.subscriber_user.client
                                             )
                qs = []
                for i in story:
                    qs.append({'title': i.title, 'url': i.url,
                               'pub_date': i.pub_date,
                               'body_text': i.body_text, 'id': i.id,
                               'company__name': i.company.all(),
                               'source__name': i.source.name})
                # cxt = {
                #     'qs': story.values('title', 'url', 'pub_date', 'body_text',
                #                        'source__name',
                #                        'company__name', 'id'),
                #     }
                return render(request, "stories/showstories.html", {'qs': qs})
            else:
                return HttpResponseRedirect("/page/add")

        else:
            cxt = {
                'error': "Invalid UserName and Password "
            }
            return render(request, 'subscribers/login.html', cxt)
    else:
        return render(request, 'subscribers/login.html')

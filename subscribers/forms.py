# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from subscribers.models import Company,Subscriber


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=10, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
         max_length=10, widget=forms.PasswordInput()
     )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',
                  'confirm_password')


class SubscriberForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    client = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = Subscriber
        fields = ('company', 'client')


                # def clean_confirm_password(self):
    #     cd = self.cleaned_data
    #     password = cd.get('password')
    #     confirm_password = cd.get('confirm_password')
    #     if password != confirm_password:
    #         raise forms.ValidationError("Password didn't match")
    #     return password
    #
    # def clean_username(self):
    #     cd = self.cleaned_data
    #     username = cd.get('username')
    #     if Subscriber.objects.filter(username__exact=username):
    #         raise forms.ValidationError("Username already exist")
    #     return username





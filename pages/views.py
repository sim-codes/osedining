from typing import Any
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView
from .forms import (ContactForm, 
                    FineDiningForm, 
                    CustomDiningForm, 
                    CasualDiningForm,
                    HireForm)
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class GalleryPageView(TemplateView):
    template_name = 'pages/gallery.html'
    

class SuccessView(TemplateView):
    template_name = 'pages/success.html'

class FineDiningSuccessful(TemplateView):
    template_name = 'menus/finedining_success.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'


class MenuView(TemplateView):
    template_name = 'pages/menu.html'


class HireAChefSuccessfulView(TemplateView):
    template_name = 'pages/hire-successful.html'

class CasualDiningSuccessfulView(TemplateView):
    template_name = 'menus/casual_successful.html'

class HireAChefView(FormView):
    form_class = HireForm
    template_name = 'pages/hire-a-chef.html'

    def post(self, request, *args, **kwargsy):
        if request.method == 'POST':
            form = HireForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('pages:hire_a_chef_success')


class CustomDiningView(FormView):
    form_class = CustomDiningForm
    template_name = 'menus/special.html'

    def post(self, request, *args, **kwargsy):
        if request.method == 'POST':
            form = CustomDiningForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('pages:customdining-successful')
            
class CustomDiningSuccessView(TemplateView):
    template_name = 'menus/special_success.html'

class FineDiningView(FormView):
    form_class = FineDiningForm
    template_name = 'menus/finedining.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = FineDiningForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('pages:finedining_success')
            

class CasualDiningView(FormView):
    form_class = CasualDiningForm
    template_name = 'menus/casualdining.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CasualDiningForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('pages:casual_successful')

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'

    # Save message and send email
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                email = form.cleaned_data['email']
                send_mail(subject, message, email, [settings.EMAIL_HOST_USER])
                return redirect('pages:success')
            else:
                return redirect('pages:contact')

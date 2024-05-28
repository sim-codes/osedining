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

    def get_success_url(self):
        return reverse('pages:success')
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')

        full_message = f'''
            Received message below from {email}, {subject}
            ---------------------------

            {message}
        '''
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=email,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)


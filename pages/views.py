from typing import Any
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView
from .forms import (ContactForm, 
                    FineDiningForm, 
                    CustomDiningForm, 
                    CasualDiningForm,
                    HireForm)
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
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

class CustomDiningSuccessView(TemplateView):
    template_name = 'menus/special_success.html'

class HireAChefView(FormView):
    form_class = HireForm
    template_name = 'pages/hire-a-chef.html'

    def post(self, request, *args, **kwargsy):
        if request.method == 'POST':
            form = HireForm(request.POST)
            if form.is_valid():
                notify_admin(form, 'hire')
                notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:hire_a_chef_success')


class CustomDiningView(FormView):
    form_class = CustomDiningForm
    template_name = 'menus/special.html'

    def post(self, request, *args, **kwargsy):
        if request.method == 'POST':
            form = CustomDiningForm(request.POST)
            if form.is_valid():
                notify_admin(form, 'Custom')
                notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:customdining-successful')

class FineDiningView(FormView):
    form_class = FineDiningForm
    template_name = 'menus/finedining.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = FineDiningForm(request.POST)
            if form.is_valid():
                notify_admin(form, 'fine')
                notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:finedining_success')
            

class CasualDiningView(FormView):
    form_class = CasualDiningForm
    template_name = 'menus/casualdining.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CasualDiningForm(request.POST)
            if form.is_valid():
                notify_admin(form, 'casual')
                notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:casual_dining_success')

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'

    # Save message and send email
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                notify_admin(form, 'contact')
                notify_user(form.cleaned_data['email'])
                return redirect('pages:success')
            else:
            # show form errors
                return render(request, 'pages/contact.html', {'form': form})


# notify user by email and the fill form
def notify_user(email):
    subject = 'Thank you for contacting us'
    message = '''
    We will get back to you shortly

    Chef Ehis
    Ose Private Dining
    +234 816 747 6771
    '''
    from_email = settings.EMAIL_HOST_USER
    to = email
    send_mail(subject, message, from_email, [to], fail_silently=True)


# notify admin by email
def notify_admin(form, dining_type):
    name = form.cleaned_data['your_name']
    subject = f'New message from {name} for {dining_type} dining'
    from_email = to = settings.EMAIL_HOST_USER
    text_content = f'{name} has requested for {dining_type} dining, below are the details:'

    html_content = f"""
    <htm>
        <head></head>
        <body>
        <p><strong>{name}</strong> has requested for <strong>{dining_type}</strong> dining, below are the details:</p>
        <table>
    """
    for key, value in form.cleaned_data.items():
        html_content += f"""
        <tr>
            <td>{key}</td>
            <td>{value}</td>
        </tr>
        """
    html_content += """
        </table>
        </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], reply_to=[form.cleaned_data['email']])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

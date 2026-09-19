from typing import Any
from datetime import date
from django.shortcuts import reverse
from django.views import View
from django.views.generic import TemplateView, FormView
from .forms import (ContactForm,
                    FineDiningForm,
                    CustomDiningForm,
                    CasualDiningForm,
                    EmberDiningForm,
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
class EmberMenuView(FormView):
    form_class = EmberDiningForm
    template_name = 'menus/ember.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = EmberDiningForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('pages:ember_menu_success')

class EmberMenuSuccessful(TemplateView):
    template_name = 'menus/ember_success.html'


EMBER_MENUS = {
    'M1': {
        'key': 'M1',
        'name': '3 Course Menu',
        'price': 90000,
        'courses': [
            {'label': 'First Course', 'dish': 'Shrimp suya arancini, smoked paprika sauce, scent leaf emulsion'},
            {'label': 'Second Course', 'dish': 'Confit duck, over egusi puree, mashed sweet potatoes, uyayaka oil'},
            {'label': 'Third Course', 'dish': 'Zozo poached pear, whipped ginger cream, zobo gel, nutty gelato'},
        ],
    },
    'M2': {
        'key': 'M2',
        'name': '4 Course Menu',
        'price': 140000,
        'courses': [
            {'label': 'First Course', 'dish': 'Deli beef suya crostini'},
            {'label': 'Second Course', 'dish': 'Avocado mousse, cassava salad, palm vinaigrette, smoked ugba aioli'},
            {'label': 'Third Course', 'dish': 'Pan seared seabass, plantain gnocchi, creamy banga gravy'},
            {'label': 'Fourth Course', 'dish': 'Spiced dark chocolate mango tart, pistachio gelato'},
        ],
    },
    'M3': {
        'key': 'M3',
        'name': '5 Course Menu',
        'price': 220000,
        'courses': [
            {'label': 'First Course', 'dish': 'Smoked black snapper pepper soup consommé, iru brioche'},
            {'label': 'Second Course', 'dish': 'Charred prawn, jollof risotto, spicy flaky plantain tuile'},
            {'label': 'Third Course', 'dish': 'Braised ehuru tozo, smoked asaro mash, coriander emulsion, amoriri gravy'},
            {'label': 'Fourth Course', 'dish': 'Lemon avo sorbet'},
            {'label': 'Fifth Course', 'dish': 'Kuli crumb, zobo caramel, trio gelato, chocolate mousse, zobo tuile'},
        ],
    },
}

SERVICE_CHARGE_RATE = 0.20


def _ember_invoice_context(request):
    menu_key = request.GET.get('menu', 'M1')
    menu = EMBER_MENUS.get(menu_key, EMBER_MENUS['M1'])

    subtotal = menu['price']
    service_charge = round(subtotal * SERVICE_CHARGE_RATE)
    total = subtotal + service_charge

    return {
        'menu': menu,
        'subtotal_display': f'{subtotal:,}',
        'service_charge_display': f'{service_charge:,}',
        'total_display': f'{total:,}',
        'generated_date': date.today().strftime('%d %B %Y'),
        'reference': f"OSE-EMB-{date.today().strftime('%y%m%d')}",
    }


class EmberInvoicePreview(View):
    def get(self, request, *args, **kwargs):
        context = _ember_invoice_context(request)
        return render(request, 'menus/ember_invoice.html', context)
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
                # notify_admin(form, 'hire')
                # notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:hire_a_chef_success')


class CustomDiningView(FormView):
    form_class = CustomDiningForm
    template_name = 'menus/special.html'

    def post(self, request, *args, **kwargsy):
        if request.method == 'POST':
            form = CustomDiningForm(request.POST)
            if form.is_valid():
                # notify_admin(form, 'Custom')
                # notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:customdining-successful')

class FineDiningView(FormView):
    form_class = FineDiningForm
    template_name = 'menus/finedining.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = FineDiningForm(request.POST)
            if form.is_valid():
                # notify_admin(form, 'fine')
                # notify_user(form.cleaned_data['email'])
                form.save()
                return redirect('pages:finedining_success')
            

class CasualDiningView(FormView):
    form_class = CasualDiningForm
    template_name = 'menus/casualdining.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CasualDiningForm(request.POST)
            if form.is_valid():
                # notify_admin(form, 'casual')
                # notify_user(form.cleaned_data['email'])
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
                # notify_admin(form, 'contact')
                # notify_user(form.cleaned_data['email'])
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

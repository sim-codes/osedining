from typing import Any
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView
from .forms import ContactForm, FineDiningForm, CustomDiningForm
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpRequest, HttpResponse


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class GalleryPageView(TemplateView):
    template_name = 'pages/gallery.html'
    

class SuccessView(TemplateView):
    template_name = 'pages/success.html'

class ReservationSuccessful(TemplateView):
    template_name = 'menus/reservation_success.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'


class MenuView(TemplateView):
    template_name = 'pages/menu.html'

class CustomDiningView(FormView):
    form_class = CustomDiningForm
    template_name = 'menus/special.html'

    def get_success_url(self) -> str:
        return reverse('pages:customdining-successful')

class CustomDiningSuccessView(TemplateView):
    template_name = 'menus/special_success.html'

class FineDiningView(FormView):
    form_class = FineDiningForm
    template_name = 'menus/finedining.html'

def make_reservation(request):
    if request.method == 'POST':
        form = FineDiningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages:reserve_success')
    else:
        form = FineDiningForm()
    return render(request, 'menus/finedining.html', {'form': form})


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


def generate_pdf_function(data):
    # Write your PDF generation code here
    html = '<html><body><head><style>\
        body {\
            font-family: Tahoma, sans-serif;\
            font-size: 12px;\
        }\
        table {\
            border-collapse: collapse;\
            width: 100%;\
        }\
        table tr:nth-child(even){background-color: #f2f2f2;}\
        td {\
            border: 1px solid black;\
            padding: 8px;\
            text-align: left;\
        }\
        </style>'
    html += '<h1>Ose Dining</h1>'
    html += '<h3>Fine Dining Invoice</h3>'
    html += '<table>'
    for key, value in data.items():
        html += '<tr>'
        html += '<td style="width:20%">' + key + '</td>'
        html += '<td>' + value + '</td>'
        html += '</tr>'
    html += '</table>'
    html += '<p>All payment should be made in favour of:<br>\
        <strong>Account Name:</strong> Ehis Foods<br>\
        <strong>Account Number:</strong> Ehis Foods<br>\
            Thanks for your patronage</p>'
    html += '</body></html>'
    result = pisa.CreatePDF(html, dest=BytesIO())
    return result


def convert_to_pdf(request):
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            data[key] = value
        del data['csrfmiddlewaretoken']
        print(data)
        result = generate_pdf_function(data)
        if result.err:
            return HttpResponse('Error generating PDF: %s' % result.err)
        response = HttpResponse(content_type='application/pdf')
        response.write(result.dest.getvalue())
        return response
    return render(request, 'menus/finedining.html')

def generate_pdf(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name', '')
        invoice_number = request.POST.get('invoice_number', '')
        invoice_date = request.POST.get('invoice_date', '')
        customer_name = request.POST.get('customer_name', '')
        customer_address = request.POST.get('customer_address', '')
        items = request.POST.get('items', '')
        # Generate PDF using xhtml2pdf
        result = generate_pdf_function(company_name, invoice_number, invoice_date, customer_name, customer_address, items)
        if result.err:
            return HttpResponse('Error generating PDF: %s' % result.err)
        response = HttpResponse(content_type='application/pdf')
        response.write(result.dest.getvalue())
        return response
    return render(request, 'menus/index.html')
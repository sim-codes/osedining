from django import forms
from captcha.fields import CaptchaField
from .models import Contact, FineReservation

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Contact
        exclude = ['date_send']


class FineDiningForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    additional_information = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5}))
    class Meta:
        model = FineReservation
        fields = ['menu_type', 'date', 'time','your_name', 'phone', 'email', 'location', 'number_of_guest', 
                  'we_are_allowed_to_take_pictures_of_you_and_your_guest',
                  'we_are_allowed_to_take_pictures_of_your_apartment',
                  'we_are_allowed_to_use_your_event_content_for_our_business_promotions',
                  'additional_information']
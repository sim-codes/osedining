from datetime import date as date_cls
from django import forms
from captcha.fields import CaptchaField
from .models import (Contact,
                     FineDining,
                     CasualDining,
                     CustomisedDining,
                     EmberDining,
                     Hire)


class FutureDateFormMixin:
    """Blocks booking a date that has already passed, both in the date picker and on submit."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in self.fields:
            self.fields['date'].widget.attrs['min'] = date_cls.today().isoformat()

    def clean_date(self):
        value = self.cleaned_data['date']
        if value < date_cls.today():
            raise forms.ValidationError('Please choose today or a future date.')
        return value


class ContactForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@email.com'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "What's this about?"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your event or question…'}))
    captcha = CaptchaField()
    class Meta:
        model = Contact
        exclude = ['date_send']


class CustomDiningForm(FutureDateFormMixin, forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = CustomisedDining
        fields = ['your_name', 'phone', 'email', 'date', 'time', 'location', 'service_details']


class FineDiningForm(FutureDateFormMixin, forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    additional_information = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5, 'placeholder':'Kindly specify any alergies or special needs.'}))
    class Meta:
        model = FineDining
        fields = ['menu_type', 'date', 'time','your_name', 'phone', 'email', 'location', 'number_of_guest', 
                  'we_are_allowed_to_take_pictures_of_you_and_your_guest',
                  'we_are_allowed_to_take_pictures_of_your_apartment',
                  'we_are_allowed_to_use_your_event_content_for_our_business_promotions',
                  'additional_information']
        


class EmberDiningForm(FutureDateFormMixin, forms.ModelForm):
    menu_type = forms.CharField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    your_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+234 800 000 0000'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder': 'you@email.com'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Event address'}))
    additional_information = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5, 'placeholder':'Kindly specify any alergies or special needs.'}))
    class Meta:
        model = EmberDining
        fields = ['menu_type', 'date', 'time','your_name', 'phone', 'email', 'location', 'number_of_guest',
                  'we_are_allowed_to_take_pictures_of_you_and_your_guest',
                  'we_are_allowed_to_take_pictures_of_your_apartment',
                  'we_are_allowed_to_use_your_event_content_for_our_business_promotions',
                  'additional_information']


class CasualDiningForm(FutureDateFormMixin, forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    additional_information = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5, 'placeholder':'Kindly specify any alergies or special needs.'}))
    class Meta:
        model = CasualDining
        fields = ['menu_type', 'date', 'time','your_name', 'phone', 'email', 
                    'location', 'number_of_guest', 'bread',
                  'side_one', 'side_two', 'vegetable_one', 'vegetable_two',
                  'we_are_allowed_to_take_pictures_of_you_and_your_guest',
                  'we_are_allowed_to_take_pictures_of_your_apartment',
                  'we_are_allowed_to_use_your_event_content_for_our_business_promotions',
                  'additional_information']

class HireForm(FutureDateFormMixin, forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    additional_information = forms.CharField(widget=forms.Textarea(
        attrs={'name':'body',
               'rows':3, 'cols':5,
               'placeholder':'Kindly specify additional information about the chef job.'}))
    class Meta:
        model = Hire
        exclude = ['date_send']

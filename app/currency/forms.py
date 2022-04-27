from currency.models import ContactUs, Rate, Source

from django import forms


class ContactusForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'subject', 'message')


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'code_name', 'url', 'social', 'logo')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('type', 'base_type', 'source', 'buy', 'sale')

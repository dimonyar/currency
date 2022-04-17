from currency.models import ContactUs, Rate, Source

from django import forms


class ContactusForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'subject', 'message')


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'url', 'ratings', 'social', 'logo')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('type', 'source', 'buy', 'sale')

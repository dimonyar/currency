from currency.models import Source

from django import forms


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url', 'fitch_ratings', 'social_items')

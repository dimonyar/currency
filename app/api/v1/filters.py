from currency.models import ContactUs, Source

import django_filters


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'name': ('exact', ),
        }


class ContactusFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'email_from': ('exact', ),
            'subject': ('exact', ),
        }

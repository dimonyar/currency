from currency.models import ContactUs, Source

from rest_framework import serializers


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'code_name',
            'social',
        )


class ContactusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'id',
            'email_from',
            'subject',
            'message',
        )

from currency.models import ContactUs, Rate, Source
from currency.tasks import sendmail_new_сontactus

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

    def create(self, validated_data):
        from_email = validated_data['email_from']
        message_body = validated_data['message']
        subject = validated_data['subject']
        sendmail_new_сontactus.delay(subject, message_body, from_email)
        return ContactUs.objects.create(**validated_data)


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'type',
            'source',
            'created',
            'buy',
            'sale',
        )

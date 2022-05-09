from api.v1.serializers import ContactusSerializer, SourceSerializer

from currency.models import ContactUs, Source

from rest_framework import generics


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactusView(generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer


class ContactusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer
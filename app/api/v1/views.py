from api.v1.serializers import ContactusSerializer, SourceSerializer

from currency.models import ContactUs, Source

from rest_framework import generics, viewsets


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactusViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer

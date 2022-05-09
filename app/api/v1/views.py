from api.v1.serializers import ContactusSerializer, SourceSerializer

from currency.models import ContactUs, Source

from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactusViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)

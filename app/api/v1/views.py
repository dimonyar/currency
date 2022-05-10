from api.v1.pagination import RatesPagination
from api.v1.serializers import ContactusSerializer, RateSerializer, SourceSerializer

from currency.models import ContactUs, Rate, Source

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


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatesPagination

from api.v1.filters import ContactusFilter, SourceFilter
from api.v1.pagination import RatesPagination
from api.v1.serializers import ContactusSerializer, RateSerializer, SourceSerializer
from api.v1.throttles import AnonCurrencyThrottle

from currency.models import ContactUs, Rate, Source

from django_filters import rest_framework as filters

from rest_framework import filters as rest_framework_filters
from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ('name',)
    throttle_classes = [AnonCurrencyThrottle]


class ContactusViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
    filterset_class = ContactusFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = ('email_from', 'subject')
    throttle_classes = [AnonCurrencyThrottle]
    search_fields = ['=email_from', 'subject', 'message']


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatesPagination
    throttle_classes = [AnonCurrencyThrottle]

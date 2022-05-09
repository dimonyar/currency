from api.v1.serializers import SourceSerializer

from currency.models import Source

from rest_framework import generics


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

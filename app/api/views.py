from rest_framework import generics
from currency.models import Source


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()

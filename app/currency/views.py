from currency.forms import RateForm, SourceForm
from currency.models import ContactUs, Rate, Source

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


# ContactUs
class ContactusList(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus.html'


# Source
class SourceList(ListView):
    queryset = Source.objects.all().order_by('-id')
    template_name = 'source_list.html'


# Source create
class SourceCreate(CreateView):
    model = Source
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


# Source update
class SourceUpdate(UpdateView):
    model = Source
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


# Source delete
class SourceDelete(DeleteView):
    model = Source
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')


# Source detail
class SourceDetail(DetailView):
    model = Source
    template_name = 'source_detail.html'


# Rate
class RateList(ListView):
    model = Rate
    template_name = 'rate_list.html'


# Rate create
class RateCreate(CreateView):
    model = Rate
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


# Rate update
class RateUpdate(UpdateView):
    model = Rate
    template_name = 'rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


# Rate delete
class RateDelete(DeleteView):
    model = Rate
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')


# Rate detail
class RateDetail(DetailView):
    model = Rate
    template_name = 'rate_detail.html'

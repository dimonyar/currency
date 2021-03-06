from currency.filters import RateFilter
from currency.forms import ContactusForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source
from currency.tasks import sendmail_new_сontactus

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import QueryDict
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from django_filters.views import FilterView


# ContactUs
class ContactusList(ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus.html'


# ContactUs Create Form
class ContactusCreate(CreateView):
    model = ContactUs
    template_name = 'contactus_create.html'
    form_class = ContactusForm
    success_url = reverse_lazy('currency:contactus')

    def form_valid(self, form):
        response = super().form_valid(form)

        data = form.cleaned_data
        subject = f"Contact us: {data['subject']}"
        message_body = f'''
        Support Email

        From: {data['email_from']}
        Message: {data['message']}
        '''
        from_email = data['email_from']

        sendmail_new_сontactus.delay(subject, message_body, from_email)

        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


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
class RateList(FilterView):
    queryset = Rate.objects.all().order_by('-id').select_related('source')
    template_name = 'rate_list.html'
    paginate_by = 5
    filterset_class = RateFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        parameters = QueryDict(mutable=True)

        for key, value in self.request.GET.items():
            if key != 'page' and value:
                parameters[key] = value
        context['filter_param'] = parameters.urlencode()
        return context


# Rate create
class RateCreate(CreateView):
    model = Rate
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


# Rate update
class RateUpdate(UserPassesTestMixin, UpdateView):
    model = Rate
    template_name = 'rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.success(self.request, 'No access for this operation. Only superuser')
        return redirect('/currency/rate/list')


# Rate delete
class RateDelete(UserPassesTestMixin, DeleteView):
    model = Rate
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.success(self.request, 'No access for this operation. Only superuser')
        return redirect('/currency/rate/list')


# Rate detail
class RateDetail(DetailView):
    model = Rate
    template_name = 'rate_detail.html'

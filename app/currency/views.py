from currency.forms import ContactusForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


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
        send_mail(
            subject,
            message_body,
            from_email,
            ['d.yaroshevsky@gmail.com'],
            fail_silently=False,
        )

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
class RateList(ListView):
    queryset = Rate.objects.all().order_by('-id').select_related('source')
    template_name = 'rate_list.html'


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

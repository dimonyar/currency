from currency.models import ContactUs, Rate

from django.shortcuts import render


# ContactUs
def contactus_list(request):
    contactus = ContactUs.objects.all()
    return render(request, 'contactus.html', context={'contactus_list': contactus})


# ContactUs
def rate_list(request):
    rate = Rate.objects.all()
    return render(request, 'rate_list.html', context={'rate_list': rate})


# Index
def index(request):
    return render(request, 'index.html')

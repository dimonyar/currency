from currency.forms import SourceForm
from currency.models import ContactUs, Rate, Source


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


# ContactUs
def contactus_list(request):
    contactus = ContactUs.objects.all()
    return render(request, 'contactus.html', context={'contactus_list': contactus})


# Rate
def rate_list(request):
    rate = Rate.objects.all()
    return render(request, 'rate_list.html', context={'rate_list': rate})


# Source
def source_list(request):
    source = Source.objects.all().order_by('-id')
    return render(request, 'source_list.html', context={'source_list': source})


# Source create
def source_create(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source_list/')
    else:
        form = SourceForm()

    return render(request, 'source_create.html', context={'form': form})


# Source update
def source_update(request, pk):
    instance = get_object_or_404(Source, pk=pk)

    if request.method == 'POST':
        form = SourceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source_list/')
    else:
        form = SourceForm(instance=instance)

    return render(request, 'source_update.html', context={'form': form})


# Source delete
def source_delete(request, pk):
    instance = get_object_or_404(Source, pk=pk)

    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect('/source_list/')
    else:
        return render(request, 'source_delete.html', context={'source': instance})


# Index
def index(request):
    return render(request, 'index.html')

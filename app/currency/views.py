from currency.models import ContactUs
from django.http import HttpResponse


# ContactUs
def contactus_list(request):
    lst = [[i.id, i.email_from, i.subject, i.message] for i in ContactUs.objects.all()]
    return HttpResponse(str(lst))

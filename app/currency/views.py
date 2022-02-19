from django.http import HttpResponse


def hell0_world(request):
    return HttpResponse('Hello World')

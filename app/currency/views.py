from django.http import HttpResponse


def hell0_world(request):
    breakpoint()
    return HttpResponse('Hello World')

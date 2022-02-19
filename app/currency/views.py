from django.http import HttpResponse


def hell0_world(request):
    breakpoint()
    print('Hello World')
    return HttpResponse('Hello World')

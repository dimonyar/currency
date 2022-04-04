from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('check-email/', TemplateView.as_view(template_name='activation.html'), name='check-email'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),

    path('currency/', include('currency.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]

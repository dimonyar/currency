from currency import views as currency_views

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('contactus/', currency_views.contactus_list),
    path('rate_list/', currency_views.rate_list),
    path('source_list/', currency_views.source_list),
    path('source_create/', currency_views.source_create),
    path('source_update/<int:pk>/', currency_views.source_update),
    path('source_delete/<int:pk>/', currency_views.source_delete),
    path('', currency_views.index),
]

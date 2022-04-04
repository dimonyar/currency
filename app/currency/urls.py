from currency import views as currency_views

from django.urls import path

app_name = 'currency'

urlpatterns = [
    path('contactus/', currency_views.ContactusList.as_view(), name="contactus"),
    path('contactus/create/', currency_views.ContactusCreate.as_view(), name="contactus_create"),

    path('rate/list/', currency_views.RateList.as_view(), name="rate_list"),
    path('rate/create/', currency_views.RateCreate.as_view(), name="rate_create"),
    path('rate/detail/<int:pk>/', currency_views.RateDetail.as_view(), name="rate_detail"),
    path('rate/update/<int:pk>/', currency_views.RateUpdate.as_view(), name="rate_update"),
    path('rate/delete/<int:pk>/', currency_views.RateDelete.as_view(), name="rate_delete"),

    path('source/list/', currency_views.SourceList.as_view(), name="source_list"),
    path('source/create/', currency_views.SourceCreate.as_view(), name="source_create"),
    path('source/detail/<int:pk>/', currency_views.SourceDetail.as_view(), name="source_detail"),
    path('source/update/<int:pk>/', currency_views.SourceUpdate.as_view(), name="source_update"),
    path('source/delete/<int:pk>/', currency_views.SourceDelete.as_view(), name="source_delete"),

]

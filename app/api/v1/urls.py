from api.v1 import views

from django.urls import path


urlpatterns = [
    path('sources/', views.SourceView.as_view(), name='sources'),
    path('contacts/', views.ContactusView.as_view(), name='contacts'),
    path('contacts/<int:pk>/', views.ContactusDetailView.as_view(), name='contacts-detail'),
]

from api.v1 import views

from django.urls import path


urlpatterns = [
    path('sources/', views.SourceView.as_view(), name='sources')
]

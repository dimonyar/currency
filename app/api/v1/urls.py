from api.v1 import views

from django.urls import path

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('contactus', views.ContactusViewSet, basename='contactus')

urlpatterns = [
    path('sources/', views.SourceView.as_view(), name='sources'),
]

urlpatterns += router.urls

from api.v1 import views

from django.urls import path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = DefaultRouter()
router.register('contactus', views.ContactusViewSet, basename='contactus')

urlpatterns = [
    path('sources/', views.SourceView.as_view(), name='sources'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls

from accounts import views

from django.contrib.auth import views as auth_views
from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('my-profile/', views.MyProfile.as_view(), name='my-profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<uuid:username>/', views.ActivateUser.as_view(), name='activate-user'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]

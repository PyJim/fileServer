from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login_user/', views.login_user, name='login'),
    path('logout/', views.logout_user),
    path('activate_user/<uidb64>/<token>/', views.activate_user, name='activate_user'),
    path('request_activation_email/', views.request_activation_email, name='request_activation_email'),
    path('reset_password/', views.reset_password),
    path('reset_password/<token>/', views.reset_password_token),
]
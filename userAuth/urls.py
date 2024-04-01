from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.login_user, name='login'),
    path('logout/', views.logout_user),
    path('activate_user/<uidb64>/<token>/', views.activate_user, name='activate_user'),
    path('request_activation_email/', views.request_activation_email, name='request_activation_email'),
    path('reset_password/', views.reset_password),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_forgotten_password/<uidb64>/<token>/', views.reset_forgotten_password, name='reset_forgotten_password'),
]
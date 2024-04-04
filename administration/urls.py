from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.signin, name='admin_login'),
    path('files/', views.files, name='files'),
    path('upload/', views.upload_file, name='upload'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.files_page, name='feed'),
    path('feed/download/<int:file_id>/', views.download_file, name='download_file'),
    path('feed/email/<int:file_id>/', views.email_file, name='email_file')

]
from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.files_page, name='files'),
    path('files/download/<int:file_id>/', views.download_file, name='download_file'),
    path('files/email/<int:file_id>/', views.email_file, name='email_file')

]
from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.files_page, name='files')
]
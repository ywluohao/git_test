from django.urls import path
from .views import start_file_generation, check_file_status

urlpatterns = [
    path('start-file-generation/', start_file_generation, name='start_file_generation'),
    path('check-file-status/', check_file_status, name='check_file_status'),
]
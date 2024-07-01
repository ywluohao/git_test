from django.urls import path
from . import views

urlpatterns = [
    path('start-file-generation/', views.start_file_generation, name='start_file_generation'),
    path('check-file-status/<str:job_id>/', views.check_file_status, name='check_file_status'),
]
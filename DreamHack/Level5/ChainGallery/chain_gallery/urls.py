from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('uploads/<path:file_path>/', views.serve_file, name='serve_file'),
    path('select/', views.process_images, name='process_images'),
    path('', views.gallery, name='gallery'),
]

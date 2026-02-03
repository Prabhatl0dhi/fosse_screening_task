from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_csv),
    path('report/', views.generate_pdf)
]

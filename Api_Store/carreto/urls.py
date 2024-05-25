from django.urls import path
from . import views

urlpatterns = [
    path('create_carreto/', views.create_carreto, name='create_carreto'),
]
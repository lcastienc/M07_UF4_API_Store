from django.urls import path
from . import views

urlpatterns = [
    path('add_client/', views.add_client, name='add_client'),
    path('', views.client_list, name='client_list'),
    path('client/<str:pk>/', views.client_detail, name='client_detail'),
    path('update_client/<str:pk>/', views.update_client, name='update_client'),
    path('delete_client/<str:pk>/', views.delete_client, name='delete_client'),
]
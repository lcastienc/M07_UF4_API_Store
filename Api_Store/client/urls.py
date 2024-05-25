from django.urls import path
from . import views

urlpatterns = [
    path('add_client', views.add_Client, name='add_client'),
    path('', views.client_list, name='client_list'),
]
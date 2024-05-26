from django.urls import path
from . import views

urlpatterns = [
    path('llista_comandes/', views.list_comandes, name='list_comandes'),
    path('comandes_client/<int:client_id>/', views.list_comandes_by_client, name='list_comandes_by_client'),
]
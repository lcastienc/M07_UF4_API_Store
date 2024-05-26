from django.urls import path
from . import views

urlpatterns = [
    path('llista_comandes/', views.list_comandes, name='list_comandes'),
]
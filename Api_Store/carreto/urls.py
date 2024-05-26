from django.urls import path
from . import views

urlpatterns = [
    path('create_carreto/', views.create_carreto, name='create_carreto'),
    path('add_product_carreto/', views.add_product_to_carreto, name='add_product_carreto'),
]
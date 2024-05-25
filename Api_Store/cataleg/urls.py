from django.urls import path
from . import views

urlpatterns = [
    path('products/add_product/', views.add_product, name='add_product'),
    path('products/update_product/<str:pk>/', views.update_product, name='update_product')
]
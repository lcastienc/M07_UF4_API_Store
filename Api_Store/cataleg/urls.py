from django.urls import path
from . import views

urlpatterns = [
    path('products/add_product/', views.add_product, name='add_product'),
    path('products/update_product/<str:pk>/', views.update_product, name='update_product'),
    path('products/update_stock_product/<str:pk>/', views.update_stock_product, name='update_stock_product'),
    path('products/delete_product/<str:pk>/', views.delete_product, name='delete_product'),
    path('products/', views.products_list, name='products_list'),
    path('products/<str:pk>', views.product_detail, name='product_detail'),

]
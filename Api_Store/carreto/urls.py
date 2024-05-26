from django.urls import path
from . import views

urlpatterns = [
    path('create_carreto/', views.create_carreto, name='create_carreto'),
    path('add_product_carreto/', views.add_product_to_carreto, name='add_product_carreto'),
    path('list_products_carreto/<int:client_id>/<int:carreto_id>/', views.list_carreto_products, name='list_carreto_products')
]
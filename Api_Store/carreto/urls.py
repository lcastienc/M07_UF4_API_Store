from django.urls import path
from . import views

urlpatterns = [
    path('create_carreto/', views.create_carreto, name='create_carreto'),
    path('add_product_carreto/', views.add_product_to_carreto, name='add_product_carreto'),
    path('delete_product_carreto/', views.delete_product_from_carreto, name='delete_product_carreto'),
    path('delete_carreto/<int:client_id>/<int:carreto_id>/', views.delete_carreto, name='delete_carreto'),
    path('update_quantity_product/', views.update_product_quantity, name='update_quantity_product'),
    path('list_products_carreto/<int:client_id>/<int:carreto_id>/', views.list_carreto_products, name='list_carreto_products'),
]
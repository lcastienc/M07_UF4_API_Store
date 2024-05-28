from django.urls import path
from . import views

urlpatterns = [
    path('pagar_comanda/', views.pagar_comanda, name='pagar_comanda'),
    path('consultar_estat_comanda/<int:comanda_id>/', views.consultar_estat_comanda, name='consultar_estat_comanda'),
]
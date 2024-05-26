from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Carreto,CarretoProduct
from .serializer import CarretoSerializer,CarretoProductSerializer
from client.models import Client
from client.serializer import ClientSerializer
from cataleg.models import Product

# Create your views here.

#crear un carrito
@api_view(['POST'])
def create_carreto(request):
    client_id = request.data.get('client_id')
    if not Client.objects.filter(id=client_id).exists():
        return Response({"error": "Cliente no encontrado"}, status=404)
    if Carreto.objects.filter(client_id=client_id, finalitzat=False).exists():
        return Response({"error": "Ya existe un carrito abierto para este cliente"}, status=400)

    carreto = Carreto.objects.create(client_id=client_id)
    serializer = CarretoSerializer(carreto)
    return Response({"status": "success", "message": "Carrito creado exitosamente", "data": serializer.data}, status=201)

#Afegir productes al carretó
@api_view(['POST'])
def add_product_to_carreto(request):
    carreto_id = request.data.get('carreto_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        carreto = Carreto.objects.get(id=carreto_id, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "No hay carrito abierto para este cliente"}, status=404)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"status": "error", "message": "Producto no encontrado"}, status=404)

    if product.stock < quantity:
        return Response({"status": "error", "message": "No hay suficiente stock disponible"}, status=400)

    # Calcular el precio total por la cantidad de productos
    total_price = product.price * quantity

    # Crear la relación CarretoProduct
    carreto_product = CarretoProduct.objects.create(carreto=carreto, product=product, quantitat=quantity, preu=total_price)

    # Actualizar el precio total del carrito
    carreto.preu_total += total_price
    carreto.save()

    # Construir la respuesta completa
    response_data = {
        "status": "success",
        "message": "Producto agregado al carrito exitosamente",
        "carreto_info": {
            "id": carreto.id,
            "client": carreto.client.id,
            "preu_total": carreto.preu_total,
            "finalitzat": carreto.finalitzat,
            "created_at": carreto.created_at,
            "updated_at": carreto.updated_at,
        },
        "product_info": {
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": quantity,
            "total_price_for_this_product": total_price
        }
    }
    return Response(response_data, status=201)


#Consultar el llistat de productes del carretó
@api_view(['GET'])
def list_carreto_products(request, client_id, carreto_id):
    if not client_id or not carreto_id:
        return Response({"status": "error", "message": "Se requiere el ID del cliente y el ID del carrito"}, status=400)

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    try:
        carreto = Carreto.objects.get(id=carreto_id, client=client, finalitzat=False)
    except Carreto.DoesNotExist:
        return Response({"status": "error", "message": "No hay carrito abierto para este cliente"}, status=404)

    carreto_serializer = CarretoSerializer(carreto)
    carreto_products = carreto.carretoproduct_set.all()
    carreto_products_serializer = CarretoProductSerializer(carreto_products, many=True)

    response_data = {
        "status": "success",
        "message": "Carrito y productos encontrados exitosamente",
        "carreto_info": carreto_serializer.data,
        "carreto_products": carreto_products_serializer.data
    }

    return Response(response_data, status=200)

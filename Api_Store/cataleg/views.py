from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product


# Create your views here.

#Afegir producte
@api_view(['POST'])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

#Actulizar un producto
@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "El producto que quieres modificar no existe"}, status=404)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": 'Producto actualizado exitosamente', "data": serializer.data}, status=200)
    return Response({"error": serializer.errors, "message": 'No se ha podido actualizar el producto'}, status=400)

#Manejo del stock del producto
@api_view(['PATCH'])
def update_stock_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "El producto que quieres actulizar el stock no existe"}, status=404)
    product.stock = request.data.get('stock',product.stock)
    product.save()
    return Response({"message": "Producto actualizado exitosamente"}, status=200)

#Borrado logico de un producto
@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=404)

    product.deleted = True
    product.save()

    return Response({"status": "success", "message": "Product marked as deleted"})
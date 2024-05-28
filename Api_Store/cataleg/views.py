from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product

# Create your views here.

#Afegir producte
@api_view(['POST'])
def add_product(request):
    # Extraer datos del request
    data = request.data
    # Verificar si el producto ya existe basado en algún campo único, por ejemplo, el nombre
    if Product.objects.filter(name=data.get('name')).exists():
        return Response({"message": "El producto ya existe"}, status=400)

    # Serializar los datos
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Producto añadido exitosamente", "data": serializer.data}, status=201)

    return Response({"error": serializer.errors, "message": "No se ha podido añadir el producto"}, status=400)

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
        return Response({"error": "El producto que quieres actualizar el stock no existe"}, status=404)

    product.stock = request.data.get('stock', product.stock)
    product.save()

    # Serializamos el producto actualizado para incluir los datos en la respuesta
    serializer = ProductSerializer(product)

    return Response({"message": "Producto actualizado exitosamente", "data": serializer.data}, status=200)


#Borrado logico de un producto
@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "El producto no existe"}, status=404)

    product.deleted = True
    product.save()

    return Response({"status": "success", "message": "Producto marcado como eliminado"}, status=200)

#Ver todos los productos
@api_view(['GET'])
def products_list(request):
    products = Product.objects.filter(deleted=False)
    serializer = ProductSerializer(products, many=True)
    return Response({"status": "success", "message": "Lista de productos obtenida exitosamente", "data": serializer.data}, status=200)


#ver informacion de un solo producto
@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk, deleted=False)
    except Product.DoesNotExist:
        return Response({"error": "El producto que buscas no existe"}, status=404)
    serializer = ProductSerializer(product)
    return Response({"status": "success", "message": "Información del producto obtenida exitosamente", "data": serializer.data}, status=200)

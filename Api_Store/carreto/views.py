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
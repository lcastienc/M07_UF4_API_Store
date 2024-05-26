from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Comanda
from .serializer import ComandaSerializer
from client.models import Client


# Create your views here.

#Mostrar historial de comandes
@api_view(['GET'])
def list_comandes(request):
    comandes = Comanda.objects.all()
    serializer = ComandaSerializer(comandes, many=True)
    return Response({"status": "success", "message": "Historial de comandes recuperado exitosamente", "data": serializer.data})

#Mostrar historial de comandes per un client en concret
@api_view(['GET'])
def list_comandes_by_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response({"status": "error", "message": "Cliente no encontrado"}, status=404)

    comandes = Comanda.objects.filter(client=client)
    serializer = ComandaSerializer(comandes, many=True)
    return Response({"status": "success", "message": "Historial de comandes del cliente recuperado exitosamente", "data": serializer.data})

#Mostrar historial de comandes que no estan finalitzades
@api_view(['GET'])
def list_open_comandes(request):
    comandes = Comanda.objects.filter(estat='Obert')
    serializer = ComandaSerializer(comandes, many=True)
    return Response({"status": "success", "message": "Historial de comandes abiertas recuperado exitosamente", "data": serializer.data})
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ClientSerializer
from .models import Client

# Create your views here.

#Register/crear un nuevo cliente/usuario
@api_view(['POST'])
def add_client(request):
    data = request.data

    # Verificar si el cliente ya existe basado en el correo electrónico
    if Client.objects.filter(email=data.get('email')).exists():
        return Response({"message": "Este cliente ya existe"}, status=400)

    # Serializar los datos
    serializer = ClientSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": 'Cliente creado exitosamente', "data": serializer.data}, status=201)

    return Response({"error": serializer.errors, "message": 'No se ha podido crear el cliente'}, status=400)

#lista de clientes
@api_view(['GET'])
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response({"status": "success", "message": "Lista de clientes obtenida exitosamente", "data": serializer.data}, status=200)

#Mostrar informacion de un cliente
@api_view(['GET'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "El cliente que buscas no existe"}, status=404)
    serializer = ClientSerializer(client)
    return Response({"status": "success", "message": "Información del cliente obtenida exitosamente", "data": serializer.data}, status=200)

#Actualizar informacion de un cliente
@api_view(['PUT'])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "El cliente que buscas no existe"}, status=404)

    serializer = ClientSerializer(client, data=request.data, partial=True)  # partial=True para permitir actualizaciones parciales
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "message": "Cliente actualizado exitosamente", "data": serializer.data}, status=200)
    return Response({"error": serializer.errors, "message": "No se ha podido actualizar el cliente"}, status=400)


#Borrar informacion de un cliente
@api_view(['DELETE'])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "El cliente que buscas no existe"}, status=404)

    client.delete()
    return Response({"status": "success", "message": "Cliente eliminado exitosamente"}, status=200)

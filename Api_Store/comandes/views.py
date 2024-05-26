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

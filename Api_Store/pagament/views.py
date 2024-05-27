from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pagament
from comandes.models import Comanda

# Create your views here.

@api_view(['POST'])
def pagar_comanda(request):
    comanda_id = request.data.get('comanda_id')
    card_number = request.data.get('card_number')
    expiry_date = request.data.get('expiry_date')
    cvc = request.data.get('cvc')

    # Verificar si la comanda está abierta
    try:
        comanda = Comanda.objects.get(id=comanda_id, estat='Obert')
    except Comanda.DoesNotExist:
        return Response({"status": "error", "message": "La comanda no está abierta"}, status=400)

    # Realizar el pago y actualizar el estado de la comanda
    payment = Pagament(comanda=comanda, card_number=card_number, data_expiration=expiry_date, cvc=cvc)
    payment.save()

    comanda.estat = 'Tancat'  # Actualizar el estado de la comanda a 'Tancat'
    comanda.save()

    return Response({"status": "success", "message": "El pago se ha realizado con éxito"}, status=200)


@api_view(['GET'])
def consultar_estat_comanda(request, comanda_id):
    try:
        comanda = Comanda.objects.get(id=comanda_id)
    except Comanda.DoesNotExist:
        return Response({"status": "error", "message": "Comanda no encontrada"}, status=404)

    return Response({"status": "success", "message": f"El estado de la comanda {comanda_id} es {comanda.estat}"}, status=200)

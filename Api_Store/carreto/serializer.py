from rest_framework import serializers
from .models import Carreto,CarretoProduct
from cataleg.models import Product
from cataleg.serializer import ProductSerializer

class CarretoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carreto
        fields = ['id', 'client', 'preu_total', 'finalitzat', 'created_at', 'updated_at']

class CarretoProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CarretoProduct
        fields = ['id', 'carreto', 'product', 'quantitat', 'preu']